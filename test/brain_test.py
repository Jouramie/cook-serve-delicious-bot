import logging
from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from core import brain
from core.brain import TaskStatement, Task, VisibleTask, TaskStatus
from suite_utils import enable_stdout_logs

enable_stdout_logs(logging.INFO)


SOME_TIME = datetime.now()
brain.CREATION_DELAY_IN_SECONDS = 0


@pytest.fixture(autouse=True)
def reset_brain_after_tests():
    yield
    brain.active_tasks = [None, None, None, None]


def test_task_visibly_waiting():
    visible_tasks = [VisibleTask(1, TaskStatus.WAITING)]

    task, callback = brain.choose_task_to_execute(visible_tasks)

    assert task is None
    assert callback is None


def test_cherry_vanilla():
    keyboard = MagicMock()
    statement = TaskStatement("Cherry Vanilla", "Two Vanilla Scoops with a Cherry, please.")
    expected_recipe = ["v", "v", "h", "enter"]
    visible_tasks = [VisibleTask(1, TaskStatus.READY)]

    _, callback = brain.choose_task_to_execute(visible_tasks)
    callback(visible_tasks, statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])


def test_the_manhattan():
    keyboard = MagicMock()
    statement = TaskStatement("The Manhattan", "Ranch, Cheese, and everything on it.")
    expected_recipe = ["r", "c", "b", "o", "m", "g", "enter"]
    visible_tasks = [VisibleTask(1, TaskStatus.READY)]

    task, callback = brain.choose_task_to_execute(visible_tasks)
    callback(visible_tasks, statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
    with freeze_time(datetime.now() + timedelta(seconds=10)):
        assert task.is_expired


def test_grey_tail_fish():
    keyboard = MagicMock()
    statement = TaskStatement("Grey Tail Fish", "Fillet the Fish, thea Season and cook.")
    expected_recipe = ["left", "down", "right", "s", "enter"]
    visible_tasks = [VisibleTask(1, TaskStatus.READY)]

    task, callback = brain.choose_task_to_execute(visible_tasks)
    callback(visible_tasks, statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
    assert task.is_cooking


def test_cooked_grey_tail_fish():
    keyboard = MagicMock()
    instructions = brain.TASKS_INSTRUCTIONS["grey tail fish"]
    cooked_task = Task(
        1,
        datetime.now(),
        TaskStatus.READY,
        TaskStatement("Grey Tail Fish", "Fillet the Fish, thea Season and cook."),
        instructions,
        datetime.now(),
    )
    brain.active_tasks[0] = cooked_task
    visible_tasks = [VisibleTask(1, TaskStatus.READY)]

    task, callback = brain.choose_task_to_execute(visible_tasks)
    callback(keyboard)

    keyboard.send.assert_has_calls([mock.call("1")])
    with freeze_time(datetime.now() + timedelta(seconds=instructions.cooking_seconds)):
        assert task.is_expired


def test_hot_bacon_pasta():
    keyboard = MagicMock()
    statement = TaskStatement("Hot Bacon Pasta", "Boil Raw Pasta...")
    expected_recipe = ["r", "enter"]
    visible_tasks = [VisibleTask(1, TaskStatus.READY)]

    with freeze_time(SOME_TIME):
        _, callback = brain.choose_task_to_execute(visible_tasks)
        callback(visible_tasks, statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
    keyboard.send.reset_mock()

    new_statement = TaskStatement("Hot Bacon Pasta", "Red Sauce, Bacon and Red Peppers")
    expected_recipe = ["r", "b", "p", "enter"]
    with freeze_time(SOME_TIME + timedelta(seconds=11)):
        _, callback = brain.choose_task_to_execute(visible_tasks)
        callback(visible_tasks, new_statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])


def test_unknown_statement():
    statement = TaskStatement("asdf", "good luck finding what to do here")
    visible_tasks = [VisibleTask(1, TaskStatus.READY)]

    with freeze_time(SOME_TIME):
        _, callback = brain.choose_task_to_execute(visible_tasks)
        execution_callback = callback(visible_tasks, statement)

    assert execution_callback.is_unknown


def test_robbery():
    keyboard = MagicMock()
    statement = TaskStatement(
        "Robbery (Witness Criminal Description)",
        "He looked crazy! Crazy eyes, but bald and normal ears/nose, long lips and a beard. Gah!",
    )
    expected_recipe = ["y", "y", "h", "e", "n", "n", "l", "f", "f", "enter"]
    visible_tasks = [VisibleTask(1, TaskStatus.READY)]

    with freeze_time(SOME_TIME):
        _, callback = brain.choose_task_to_execute(visible_tasks)
        callback(visible_tasks, statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
