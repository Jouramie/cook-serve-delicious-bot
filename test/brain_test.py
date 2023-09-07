from unittest import mock
from unittest.mock import MagicMock

from core import brain
from core.brain import TaskStatement


def test_cherry_vanilla():
    keyboard = MagicMock()
    statement = TaskStatement("Cherry Vanilla", "Two Vanilla Scoops with a Cherry, please.")
    expected_recipe = ["v", "v", "h", "enter"]

    instruction = brain.new_task_callback([1], statement)
    instruction(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])


def test_the_manhattan():
    keyboard = MagicMock()
    statement = TaskStatement("The Manhattan", "Ranch, Cheese, and everything on it.")
    expected_recipe = ["r", "c", "b", "o", "m", "g", "enter"]

    instruction = brain.new_task_callback([1], statement)
    instruction(keyboard)

    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
