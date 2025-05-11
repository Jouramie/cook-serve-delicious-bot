from unittest import mock
from unittest.mock import MagicMock

import pytest

from core import brain
from core.brain import TaskStatement

brain.CREATION_DELAY_IN_SECONDS = 0


@pytest.fixture(autouse=True)
def reset_brain_after_tests():
    yield
    brain.active_tasks = [None, None, None, None]


def test_jumbo_diet():
    keyboard = MagicMock()
    statement = TaskStatement("Jumbo Diet", "A Jumbo Diet with Ice, please.")
    expected_recipe = ["up", "up", "up", "left", "down", "i", "enter"]

    callback = brain.choose_task_to_execute([1])
    callback([1], statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])


def test_jumbo_diet_flavor():
    keyboard = MagicMock()
    statement = TaskStatement("Jumbo Diet w/Flavor Blast", "A Jumbo Diet with Ice and Flavor Blast, please.")
    expected_recipe = ["up", "up", "up", "left", "down", "i", "f", "enter"]

    callback = brain.choose_task_to_execute([1])
    callback([1], statement)(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
