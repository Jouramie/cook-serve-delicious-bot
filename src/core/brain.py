import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib.resources import files
from typing import Callable, Protocol

from core import resources

logger = logging.getLogger(__name__)

# TODO pickle?
with files(resources).joinpath("tasks.json").open() as recipes_file:
    tasks: dict = json.load(recipes_file)


@dataclass
class TaskStatement:
    title: str
    description: str


class Keyboard(ABC):
    @abstractmethod
    def send(self, key):
        raise NotImplementedError

    @abstractmethod
    def wait_for(self, key):
        raise NotImplementedError


class Instruction(Protocol):
    def __call__(self, keyboard: Keyboard):
        raise NotImplementedError


@dataclass
class StepsInstruction:
    steps: list[str]

    def __call__(self, keyboard: Keyboard):
        for s in self.steps:
            keyboard.send(s)


class UnknownTaskInstruction:
    def __call__(self, keyboard: Keyboard):
        keyboard.wait_for("enter")


@dataclass
class SimpleTaskInstruction:
    keys: list[str]

    def __call__(self, keyboard: Keyboard):
        logger.info(f"Executing '{self.keys}'.")
        for key in self.keys:
            keyboard.send(key)
        time.sleep(1)


def choose_task_to_execute(
    waiting_tasks: list[int],
) -> tuple[int, Callable[[list[int], TaskStatement | None], Instruction]]:
    return waiting_tasks[0], new_task_callback


def new_task_callback(waiting_tasks: list[int], statement: TaskStatement) -> Instruction:
    task = tasks.get(statement.title)
    if task is None:
        logger.warning(f"'{statement.title}' is unknown. How am I supposed to '{statement.description}'??")
        return UnknownTaskInstruction()

    logger.info(f"I know how to '{statement.title}'! Just '{str(task['keys'])}'.")
    return SimpleTaskInstruction(task["keys"].split(","))
