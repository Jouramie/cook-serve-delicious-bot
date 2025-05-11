from __future__ import annotations

import enum
import json
import logging
import re
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from importlib.resources import files
from typing import Any, Pattern, Protocol, runtime_checkable, ClassVar

from black.linegen import partial

from core import resources

EXPIRATION_DELAY_IN_SECONDS = 1
CREATION_DELAY_IN_SECONDS = 1

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

active_tasks: list[Task | None] = [None, None, None, None]


def define_callback(func: Callable = None, /, *, is_executable: bool = True, is_unknown: bool = False):
    if not func:
        return partial(define_callback, is_executable=is_executable)

    setattr(func, "is_executable", is_executable)
    setattr(func, "is_unknown", is_unknown)
    return func


@dataclass
class TaskStatement:
    title: str
    description: str


class TaskType(enum.Enum):
    SIMPLE = enum.auto()
    COOKING = enum.auto()
    UNKNOWN = enum.auto()


@dataclass
class HoldInput:
    key: str
    hold_seconds: float


@dataclass
class TaskInstructions:
    type: TaskType
    keys: list[str | HoldInput] | None = None
    cooking_seconds: int | None = None
    input_delay_seconds: float = 0
    post_task_seconds: float = 0
    has_next_step: bool = False

    @staticmethod
    def from_dict(d: dict[str, Any]):
        keys = []
        for input_ in d["keys"].split(","):
            split_input = input_.split(":")
            if len(split_input) == 1:
                keys.append(input_)
                continue

            input_mode, *args = split_input
            if input_mode == "hold":
                key, hold_seconds = args
                keys.append(HoldInput(key, float(hold_seconds)))
            else:
                raise Exception(f"Unknown input mode '{input_mode}'")

        return TaskInstructions(
            TaskType[d.get("type", TaskType.SIMPLE.name)],
            keys,
            d.get("cooking_seconds"),
            d.get("input_delay_seconds", 0),
            d.get("post_task_seconds", 0),
        )

    @staticmethod
    def unknown():
        return TaskInstructions(TaskType.UNKNOWN)

    def get_executions(self, task: Task):
        if self.type == TaskType.UNKNOWN:
            return task.unknown_task_execution

        if self.type == TaskType.COOKING:
            logger.info(
                f"I know how to '{task.statement.title}'! "
                f"Just {str(self.keys)}, then cook for {str(self.cooking_seconds)} seconds."
            )
            task.has_next_step = self.has_next_step
            return task.cooking_task_execution

        logger.info(f"I know how to '{task.statement.title}'! Just {str(self.keys)}.")
        return task.simple_task_execution


@dataclass
class EquipmentStep:
    SPECIAL_KEYWORDS: ClassVar[list[str]] = ["(2x)", "(3x)"]

    type: TaskType
    keys: dict[str, list[str]]
    step_format: Pattern[str] | None = None
    step_keywords: list[str] | None = None
    cooking_seconds: int | None = None
    serve_at_end: bool = True

    def __post_init__(self):
        if self.step_keywords is not None:
            self.step_keywords += self.SPECIAL_KEYWORDS

    @staticmethod
    def from_dict(d: dict[str, Any]):
        return EquipmentStep(
            TaskType[d.get("type", TaskType.SIMPLE.name)],
            d["keys"],
            re.compile(d["step_format"]) if "step_format" in d else None,
            d["step_keywords"] if "step_keywords" in d else None,
            d["cooking_seconds"] if "cooking_seconds" in d else None,
        )

    def find_instructions(self, description: str) -> TaskInstructions | None:
        if self.step_format is not None:
            task_elements = self._find_task_elements_by_format(description)
        else:
            task_elements = self._find_task_elements_by_keywords(description)

        if task_elements is None:
            return None

        logger.info(f"Found {task_elements} elements.")
        keys = []
        for task_element, next_element in zip(task_elements, task_elements[1:] + [None]):
            if task_element in self.SPECIAL_KEYWORDS:
                continue

            if next_element == "(3x)":
                n = 3
            elif next_element == "(2x)":
                n = 2
            else:
                n = 1

            keys += [key for key in self.keys[task_element]] * n

        if self.serve_at_end:
            keys.append("enter")

        return TaskInstructions(self.type, keys, cooking_seconds=self.cooking_seconds)

    def _find_task_elements_by_format(self, description: str) -> list[str] | None:
        match = self.step_format.match(description)
        if match is None or not any(match.groups()):
            return None

        logger.info(f"Found {match.groups()}.")
        return [task_element for task_element in match.groups() if task_element is not None]

    def _find_task_elements_by_keywords(self, description: str) -> list[str] | None:
        return sorted(
            [keyword for keyword in self.step_keywords if keyword in description], key=lambda x: description.index(x)
        )


@dataclass
class Equipment:
    name: str
    title_keywords: list[str]
    steps: list[EquipmentStep]

    @staticmethod
    def from_dict(name: str, d: dict[str, Any]):
        return Equipment(name, d["title_keywords"], [EquipmentStep.from_dict(step) for step in d["steps"]])

    def match_title(self, title: str) -> bool:
        return any(keyword in title for keyword in self.title_keywords)

    def find_instructions(self, description: str) -> TaskInstructions | None:
        for i, step in enumerate(self.steps):
            instructions = step.find_instructions(description)
            if instructions is None:
                logger.info(f"Skipping '{step.type.name}' step as description did not match.")
                continue

            if i != len(self.steps) - 1:
                instructions.has_next_step = True

            return instructions


@runtime_checkable
class TaskExecutionCallback(Protocol):
    is_unknown: ClassVar[bool]
    is_executable: ClassVar[bool] = True

    def __call__(self, keyboard: Keyboard) -> None:
        raise NotImplementedError


@runtime_checkable
class ReadStatementCallback(Protocol):
    is_executable: ClassVar[bool] = False

    def __call__(self, waiting_tasks: list[int], statement: TaskStatement) -> TaskExecutionCallback:
        raise NotImplementedError


@dataclass
class Task:
    index: int
    created_at: datetime
    statement: TaskStatement | None = None
    instructions: TaskInstructions | None = None
    cooked_at: datetime | None = None
    expire_at: datetime | None = None
    missed_one_check: bool = False
    has_next_step: bool = False

    def get_executions(self, statement: TaskStatement, instructions: TaskInstructions):
        self.statement = statement
        self.instructions = instructions
        return instructions.get_executions(self)

    @property
    def is_new(self) -> bool:
        return self.statement is None

    @property
    def is_cooking(self) -> bool:
        return not self.is_new and self.instructions.type == TaskType.COOKING and self.cooked_at > datetime.now()

    @property
    def is_cooked(self) -> bool:
        return not self.is_new and self.instructions.type == TaskType.COOKING and self.cooked_at <= datetime.now()

    @property
    def is_expired(self) -> bool:
        return self.is_completed and self.expire_at <= datetime.now()

    @property
    def is_completed(self) -> bool:
        return self.expire_at is not None

    @property
    def is_ready(self) -> bool:
        return not self.is_completed and (
            (self.is_new and self.created_at + timedelta(seconds=CREATION_DELAY_IN_SECONDS) <= datetime.now())
            or self.is_cooked
        )

    @property
    def is_just_arrived(self) -> bool:
        return self.created_at + timedelta(seconds=CREATION_DELAY_IN_SECONDS) > datetime.now()

    def complete(self):
        self.expire_at = datetime.now() + timedelta(seconds=EXPIRATION_DELAY_IN_SECONDS)

    def cook(self):
        self.cooked_at = datetime.now() + timedelta(seconds=self.instructions.cooking_seconds)
        logger.info(f"{self.statement.title} will be cooked at {self.cooked_at}.")

    @define_callback(is_unknown=True)
    def unknown_task_execution(self, keyboard: Keyboard) -> None:
        keyboard.wait_for("enter")
        self.complete()

    @define_callback
    def simple_task_execution(self, keyboard: Keyboard) -> None:
        logger.info(f"Executing '{self.instructions.keys}'.")
        for key in self.instructions.keys:
            keyboard.send(key)
            if self.instructions.input_delay_seconds != 0:
                time.sleep(self.instructions.input_delay_seconds)
        self.complete()
        if self.instructions.post_task_seconds != 0:
            time.sleep(self.instructions.post_task_seconds)

    @define_callback
    def cooking_task_execution(self, keyboard: Keyboard) -> None:
        logger.info(f"Executing '{self.instructions.keys}'.")
        for key in self.instructions.keys:
            keyboard.send(key)
        self.cook()

    @define_callback
    def serve_execution(self, keyboard: Keyboard) -> None:
        logger.info(f"Executing '{str(self.index)}'.")
        keyboard.send(str(self.index))
        self.complete()

    @define_callback(is_executable=False)
    def read_statement_callback(self, waiting_tasks: list[int], statement: TaskStatement) -> TaskExecutionCallback:
        _synchronize_waiting_tasks(waiting_tasks)

        instructions = TASKS_INSTRUCTIONS.get(statement.title)
        if instructions is not None:
            return self.get_executions(statement, instructions)

        logger.info(
            f"'{statement.title}' is not in predefined tasks. Trying to interpret statement '{statement.description}'."
        )
        for equipment in EQUIPMENTS.values():
            if not equipment.match_title(statement.title):
                continue

            logger.info(f"'{statement.title}' is a '{equipment.name}' task.")
            instructions = equipment.find_instructions(statement.description)
            if instructions is None:
                logger.warning(f"'Could not understand instructions for {statement.title}.")
                break
            return self.get_executions(statement, instructions)

        logger.warning(f"'{statement.title}' is unknown. How am I supposed to '{statement.description}'??")
        return self.get_executions(statement, TaskInstructions.unknown())


class Keyboard(ABC):
    @abstractmethod
    def send(self, key: str | HoldInput):
        raise NotImplementedError

    @abstractmethod
    def wait_for(self, key: str):
        raise NotImplementedError


with files(resources).joinpath("tasks.json").open() as recipes_file:
    TASKS_INSTRUCTIONS: dict[str, TaskInstructions] = {
        k: TaskInstructions.from_dict(v) for k, v in json.load(recipes_file).items()
    }

with files(resources).joinpath("equipments.json").open() as equipments_file:
    EQUIPMENTS: dict[str, Equipment] = {k: Equipment.from_dict(k, v) for k, v in json.load(equipments_file).items()}

    @property
    def index(self):
        return self.task.index


def _synchronize_waiting_tasks(waiting_tasks: list[int]):
    global active_tasks
    logger.info(f"Tasks {waiting_tasks} are waiting.")
    for i in range(len(active_tasks)):
        logger.debug(f"Task {i + 1}: {active_tasks[i]}")

        active_task = active_tasks[i]
        if active_task is None:
            if i + 1 in waiting_tasks:
                active_tasks[i] = Task(i + 1, datetime.now())
            continue

        if active_task.is_expired:
            active_tasks[i] = None
            continue

        if i + 1 not in waiting_tasks and not active_task.is_just_arrived:
            logger.info(f"Task {i + 1} does not seems to still be waiting...")
            if active_task.missed_one_check:
                active_tasks[i] = None
                continue
            active_task.missed_one_check = True


def choose_task_to_execute(
    waiting_tasks: list[int],
) -> tuple[Task | None, ReadStatementCallback | TaskExecutionCallback | None]:
    global active_tasks

    _synchronize_waiting_tasks(waiting_tasks)

    chosen_task = next((t for t in active_tasks if t is not None and t.is_ready), None)
    if chosen_task is None:
        return None, None

    if chosen_task.is_cooked and not chosen_task.has_next_step:
        return chosen_task, chosen_task.serve_execution

    return chosen_task, chosen_task.read_statement_callback
