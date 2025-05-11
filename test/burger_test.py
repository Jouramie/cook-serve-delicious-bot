from datetime import datetime, timedelta

SOME_TIME = datetime.now()
from unittest import mock
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from core import brain
from core.brain import TaskStatement

brain.CREATION_DELAY_IN_SECONDS = 0


@pytest.fixture(autouse=True)
def reset_brain_after_tests():
    yield
    brain.active_tasks = [None, None, None, None]


def test_blt():
    keyboard = MagicMock()
    statement = TaskStatement("BLT", "Bacon, Lettuce and Tomatoes")
    expected_recipe = ["b", "l", "t", "enter"]

    _, callback = brain.choose_task_to_execute([1])
    callback([1], statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])


def test_the_red():
    keyboard = MagicMock()
    statement = TaskStatement("The RED", "One meat patty...")
    expected_recipe = ["m", "enter"]

    with freeze_time(SOME_TIME):
        _, callback = brain.choose_task_to_execute([1])
        callback([1], statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
    keyboard.send.reset_mock()

    new_statement = TaskStatement("The RED", "Meat and Tomatoes only, please.")
    expected_recipe = ["m", "t", "enter"]
    with freeze_time(SOME_TIME + timedelta(seconds=9)):
        _, callback = brain.choose_task_to_execute([1])
        callback([1], new_statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])


def test_the_triple():
    keyboard = MagicMock()
    statement = TaskStatement("The Triple", "Three meat patties...")
    expected_recipe = ["m", "m", "m", "enter"]

    with freeze_time(SOME_TIME):
        _, callback = brain.choose_task_to_execute([1])
        callback([1], statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
    keyboard.send.reset_mock()

    new_statement = TaskStatement("The Triple", "Meat (3x) and Cheese")
    expected_recipe = ["m", "m", "m", "c", "enter"]
    with freeze_time(SOME_TIME + timedelta(seconds=9)):
        _, callback = brain.choose_task_to_execute([1])
        callback([1], new_statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
