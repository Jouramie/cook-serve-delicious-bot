import logging
import sys
from unittest import mock
from unittest.mock import MagicMock

import cv2
import pytest

from core import brain, sensor
from kit import img_logger

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)
brain.CREATION_DELAY_IN_SECONDS = 0


@pytest.fixture(autouse=True)
def reset_brain_after_tests():
    yield
    brain.active_tasks = [None, None, None, None]


def test_jumbo_cola_extra_onions():
    task, statement_callback = brain.choose_task_to_execute([4])

    try:
        img = cv2.cvtColor(cv2.imread(r"resources/jumbo_cola_extra_onions.tiff"), cv2.COLOR_BGR2RGB)

        statement = sensor.read_task_statement(img)
        assert statement.title == "Jumbo Cola"
    finally:
        img_logger.finalize()

    keyboard = MagicMock()

    execution_callback = statement_callback([4], statement)
    execution_callback(keyboard)

    expected_recipe = ["up", "up", "up", "down", "i", "enter"]
    keyboard.send.assert_has_calls([mock.call(key) for key in expected_recipe])
