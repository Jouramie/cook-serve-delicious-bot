import logging
from unittest import mock
from unittest.mock import MagicMock

import cv2
import pytest

from botkit import img_logger
from core import brain, sensor
from core.brain import VisibleTask, TaskStatus
from suite_utils import enable_stdout_logs

enable_stdout_logs(logging.INFO)
brain.CREATION_DELAY_IN_SECONDS = 0


@pytest.fixture(autouse=True)
def reset_brain_after_tests():
    yield
    brain.active_tasks = [None, None, None, None, None, None]


def test_jumbo_cola_extra_onions():
    visible_tasks = [None, None, None, VisibleTask(4, TaskStatus.READY)]

    task, statement_callback = brain.choose_task_to_execute(visible_tasks)

    try:
        img = cv2.cvtColor(cv2.imread(r"resources/correction/jumbo_cola_extra_onions.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Jumbo Cola"
    finally:
        img_logger.finalize()

    keyboard = MagicMock()

    execution_callback = statement_callback(visible_tasks, frame.current_statement)
    execution_callback(keyboard)

    expected_recipe = ["up", "up", "up", "down", "i", "enter"]
    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])


def test_pepters_pasta():
    visible_tasks = [None, VisibleTask(2, TaskStatus.WAITING), None, None, VisibleTask(5, TaskStatus.READY), None]

    task, statement_callback = brain.choose_task_to_execute(visible_tasks)

    try:
        img = cv2.cvtColor(cv2.imread(r"resources/correction/pepters_pasta.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Cheesy Deluxe Pasta"
    finally:
        img_logger.finalize()

    keyboard = MagicMock()

    execution_callback = statement_callback(visible_tasks, frame.current_statement)
    execution_callback(keyboard)

    expected_recipe = ["c", "m", "k", "b", "p", "u", "s", "o", "enter"]
    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])


def test_sushi():
    visible_tasks = [
        VisibleTask(1, TaskStatus.READY),
        VisibleTask(2, TaskStatus.WAITING),
        None,
        VisibleTask(4, TaskStatus.WAITING),
    ]
    task, statement_callback = brain.choose_task_to_execute(visible_tasks)

    try:
        img = cv2.cvtColor(cv2.imread(r"resources/sushi.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Mixed Delicious"
    finally:
        img_logger.finalize()

    keyboard = MagicMock()
    execution_callback = statement_callback(visible_tasks, frame.current_statement)
    execution_callback(keyboard)

    expected_recipe = ["e", "e", "r", "r", "r", "t", "t", "u", "enter"]
    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
