from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Protocol


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


class WaitTaskCompletedInstruction:
    def __call__(self, keyboard: Keyboard):
        keyboard.wait_for("enter")


def choose_task_to_execute(
    waiting_tasks: list[int],
) -> tuple[int, Callable[[list[int], TaskStatement | None], Instruction]]:
    return waiting_tasks[0], new_task_callback


def new_task_callback(waiting_tasks: list[int], statement: TaskStatement) -> Instruction:
    return WaitTaskCompletedInstruction()
