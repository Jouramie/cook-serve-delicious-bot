import logging
import sys

import cv2

from botkit import img_logger
from core import sensor

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)


def test_medium_grape_w_flavor_blast():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-grape-w-flavor-blast.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame)

        assert frame.tasks == {
            2: {"status": "ready"},
            3: {"status": "ready"},
            4: {"status": "ready"},
        }

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_1.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame)

        assert frame.tasks == {
            1: {"status": "ready"},
            2: {"status": "ready"},
            3: {"status": "ready"},
        }

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame)

        assert frame.tasks == {
            1: {"status": "ready"},
            2: {"status": "ready"},
            3: {"status": "ready"},
        }

    finally:
        img_logger.finalize()


def test_task_2_blink_rush_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-2-blink-rush-1.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame)

        assert frame.tasks == {
            1: {"status": "waiting"},
            2: {"status": "ready"},
        }

    finally:
        img_logger.finalize()


def test_task_2_blink_rush_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-2-blink-rush-2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame)

        assert frame.tasks == {
            1: {"status": "waiting"},
            2: {"status": "ready"},
        }

    finally:
        img_logger.finalize()


def test_5_tasks():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/5-tasks.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame)

        assert frame.tasks == {
            1: {"status": "waiting"},
            3: {"status": "waiting"},
            5: {"status": "ready"},
        }

    finally:
        img_logger.finalize()


def test_tasks_3_waiting_under_cola_machine():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/jumbo_cola_extra_onions.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame, log_steps="cola")

        assert frame.tasks == {
            1: {"status": "waiting"},
            3: {"status": "waiting"},
            4: {"status": "ready"},
        }

    finally:
        img_logger.finalize()


def test_tasks_1_2_waiting():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-1-2-waiting.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame)

        assert frame.tasks == {
            1: {"status": "waiting"},
            2: {"status": "waiting"},
        }

    finally:
        img_logger.finalize()


def test_task_2_waiting():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-2-waiting.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame)

        assert frame.tasks == {
            2: {"status": "waiting"},
            3: {"status": "ready"},
        }

    finally:
        img_logger.finalize()


def test_tasks_waiting_during_date():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/date/tasks-waiting-during-date.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame)

        assert frame.tasks == {
            2: {"status": "ready"},
            3: {"status": "waiting"},
            4: {"status": "waiting"},
            5: {"status": "waiting"},
        }

    finally:
        img_logger.finalize()


def test_task_1_waiting():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-1-waiting.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.find_waiting_tasks(frame, log_steps="task_1_waiting")

        assert frame.tasks == {
            1: {"status": "waiting"},
        }

    finally:
        img_logger.finalize()
