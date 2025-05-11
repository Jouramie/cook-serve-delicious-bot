from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from core import brain
from core.brain import TaskStatement, Task

brain.CREATION_DELAY_IN_SECONDS = 0


@pytest.fixture(autouse=True)
def reset_brain_after_tests():
    yield
    brain.active_tasks = [None, None, None, None]


def test_cherry_vanilla():
    keyboard = MagicMock()
    statement = TaskStatement("Cherry Vanilla", "Two Vanilla Scoops with a Cherry, please.")
    expected_recipe = ["v", "v", "h", "enter"]

    _, callback = brain.choose_task_to_execute([1])
    callback([1], statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])


def test_the_manhattan():
    keyboard = MagicMock()
    statement = TaskStatement("The Manhattan", "Ranch, Cheese, and everything on it.")
    expected_recipe = ["r", "c", "b", "o", "m", "g", "enter"]

    task, callback = brain.choose_task_to_execute([1])
    callback([1], statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
    with freeze_time(datetime.now() + timedelta(seconds=10)):
        assert task.is_expired


def test_grey_tail_fish():
    keyboard = MagicMock()
    statement = TaskStatement("Grey Tail Fish", "Fillet the Fish, thea Season and cook.")
    expected_recipe = ["left", "down", "right", "s", "enter"]

    task, callback = brain.choose_task_to_execute([1])
    callback([1], statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
    assert task.is_cooking


def test_cooked_grey_tail_fish():
    keyboard = MagicMock()
    instructions = brain.TASKS_INSTRUCTIONS["Grey Tail Fish"]
    cooked_task = Task(
        1,
        datetime.now(),
        TaskStatement("Grey Tail Fish", "Fillet the Fish, thea Season and cook."),
        instructions,
        datetime.now(),
    )
    brain.active_tasks[0] = cooked_task

    task, callback = brain.choose_task_to_execute([1])
    callback(keyboard)

    keyboard.send.assert_has_calls([mock.call("1")])
    with freeze_time(datetime.now() + timedelta(seconds=instructions.cooking_seconds)):
        assert task.is_expired
