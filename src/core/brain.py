from __future__ import annotations

import enum
import json
import logging
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from importlib.resources import files
from typing import Any, Pattern

from core import resources

EXPIRATION_DELAY_IN_SECONDS = 1
CREATION_DELAY_IN_SECONDS = 1

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

active_tasks: list[Task | None] = [None, None, None, None]


@dataclass
class TaskStatement:
    title: str
    description: str


class TaskType(enum.Enum):
    SIMPLE = enum.auto()
    COOKING = enum.auto()
    UNKNOWN = enum.auto()


@dataclass
class TaskInstructions:
    type: TaskType
    keys: list[str] | None = None
    cooking_seconds: int | None = None
    input_delay_seconds: float = 0
    post_task_seconds: float = 0

    @staticmethod
    def from_dict(d: dict[str, Any]):
        return TaskInstructions(
            TaskType[d.get("type", TaskType.SIMPLE.name)],
            d["keys"].split(","),
            d.get("cooking_seconds"),
            d.get("input_delay_seconds", 0),
            d.get("post_task_seconds", 0),
        )

    @staticmethod
    def unknown():
        return TaskInstructions(TaskType.UNKNOWN)

    def get_executions(self, task: Task):
        if self.type == TaskType.UNKNOWN:
            return UnknownTaskExecution(task)

        if self.type == TaskType.COOKING:
            logger.info(
                f"I know how to '{task.statement.title}'! "
                f"Just '{str(self.keys)}', then cook for {str(self.cooking_seconds)} seconds."
            )
            return CookingTaskExecution(task)

        logger.info(f"I know how to '{task.statement.title}'! Just '{str(self.keys)}'.")
        return SimpleTaskExecution(task)


@dataclass
class Equipment:
    name: str
    title_keywords: list[str]
    task_format: Pattern[str]
    keys: dict[str, list[str]]

    @staticmethod
    def from_dict(name: str, d: dict[str, Any]):
        return Equipment(name, d["title_keywords"], re.compile(d["task_format"]), d["keys"])

    def match_title(self, title: str) -> bool:
        return any(keyword in title for keyword in self.title_keywords)

    def find_instructions(self, description: str) -> TaskInstructions | None:
        match = self.task_format.match(description)
        if match is None:
            return None

        logger.info(f"Found {match.groups()}.")
        return TaskInstructions(
            TaskType.SIMPLE,
            [key for task_element in match.groups() if task_element is not None for key in self.keys[task_element]]
            + self.keys["Serve"],
        )


@dataclass
class Task:
    index: int
    created_at: datetime
    statement: TaskStatement | None = None
    instructions: TaskInstructions | None = None
    cooked_at: datetime | None = None
    expire_at: datetime | None = None
    missed_one_check: bool = False

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


class Keyboard(ABC):
    @abstractmethod
    def send(self, key):
        raise NotImplementedError

    @abstractmethod
    def wait_for(self, key):
        raise NotImplementedError


class TaskExecution:
    def __call__(self, keyboard: Keyboard):
        raise NotImplementedError


@dataclass
class UnknownTaskExecution(TaskExecution):
    task: Task

    def __call__(self, keyboard: Keyboard):
        keyboard.wait_for("enter")
        self.task.complete()


@dataclass
class SimpleTaskExecution(TaskExecution):
    task: Task

    def __call__(self, keyboard: Keyboard):
        logger.info(f"Executing '{self.task.instructions.keys}'.")
        for key in self.task.instructions.keys:
            keyboard.send(key)
            if self.task.instructions.input_delay_seconds != 0:
                time.sleep(self.task.instructions.input_delay_seconds)
        self.task.complete()
        if self.task.instructions.post_task_seconds != 0:
            time.sleep(self.task.instructions.post_task_seconds)


@dataclass
class CookingTaskExecution(TaskExecution):
    task: Task

    def __call__(self, keyboard: Keyboard):
        logger.info(f"Executing '{self.task.instructions.keys}'.")
        for key in self.task.instructions.keys:
            keyboard.send(key)
        self.task.cook()


@dataclass
class ServeExecution(TaskExecution):
    task: Task

    def __call__(self, keyboard: Keyboard):
        logger.info(f"Executing '{str(self.task.index)}'.")
        keyboard.send(str(self.task.index))
        self.task.complete()


with files(resources).joinpath("tasks.json").open() as recipes_file:
    TASKS_INSTRUCTIONS: dict[str, TaskInstructions] = {
        k: TaskInstructions.from_dict(v) for k, v in json.load(recipes_file).items()
    }

with files(resources).joinpath("equipments.json").open() as equipments_file:
    EQUIPMENTS: dict[str, Equipment] = {k: Equipment.from_dict(k, v) for k, v in json.load(equipments_file).items()}


@dataclass
class StatementCallback:
    task: Task

    def __call__(self, waiting_tasks: list[int], statement: TaskStatement) -> TaskExecution:
        _synchronize_waiting_tasks(waiting_tasks)

        instructions = TASKS_INSTRUCTIONS.get(statement.title)
        if instructions is not None:
            return self.task.get_executions(statement, instructions)

        logger.info(f"'{statement.title}' is unknown. Trying to interpret the task from '{statement.description}'.")
        for equipment in EQUIPMENTS.values():
            if not equipment.match_title(statement.title):
                continue

            logger.info(f"'{statement.title}' is a '{equipment.name}' task.")
            instructions = equipment.find_instructions(statement.description)
            if instructions is None:
                logger.warning(f"'Could not understand instructions for {statement.title}.")
                break
            return self.task.get_executions(statement, instructions)

        logger.warning(f"'{statement.title}' is unknown. How am I supposed to '{statement.description}'??")
        return self.task.get_executions(statement, TaskInstructions.unknown())

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
) -> StatementCallback | ServeExecution | None:
    global active_tasks

    _synchronize_waiting_tasks(waiting_tasks)

    chosen_task = next((t for t in active_tasks if t is not None and t.is_ready), None)
    if chosen_task is None:
        return None

    if chosen_task.is_cooked:
        return ServeExecution(chosen_task)

    return StatementCallback(chosen_task)
