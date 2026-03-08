import logging

import cv2
import pytest

from botkit import img_logger
from core import sensor
from core.brain import TaskStatus, VisibleTask
from suite_utils import enable_stdout_logs

enable_stdout_logs(logging.INFO)


def test_medium_grape_w_flavor_blast():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-grape-w-flavor-blast.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            None,
            VisibleTask(2, TaskStatus.READY),
            VisibleTask(3, TaskStatus.READY),
            VisibleTask(4, TaskStatus.READY),
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_1.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            VisibleTask(1, TaskStatus.READY),
            VisibleTask(2, TaskStatus.READY),
            VisibleTask(3, TaskStatus.READY),
            None,
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            VisibleTask(1, TaskStatus.READY),
            VisibleTask(2, TaskStatus.READY),
            VisibleTask(3, TaskStatus.READY),
            None,
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_task_2_blink_rush_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-2-blink-rush-1.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            VisibleTask(1, TaskStatus.WAITING),
            VisibleTask(2, TaskStatus.READY),
            None,
            None,
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_task_2_blink_rush_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-2-blink-rush-2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            VisibleTask(1, TaskStatus.WAITING),
            VisibleTask(2, TaskStatus.READY),
            None,
            None,
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_5_tasks():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/5-tasks.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            VisibleTask(1, TaskStatus.WAITING),
            None,
            VisibleTask(3, TaskStatus.WAITING),
            None,
            VisibleTask(5, TaskStatus.READY),
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_tasks_3_waiting_under_cola_machine():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/correction/jumbo_cola_extra_onions.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            VisibleTask(1, TaskStatus.WAITING),
            None,
            VisibleTask(3, TaskStatus.WAITING),
            VisibleTask(4, TaskStatus.READY),
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_tasks_1_2_waiting():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-1-2-waiting.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            VisibleTask(1, TaskStatus.WAITING),
            VisibleTask(2, TaskStatus.WAITING),
            None,
            None,
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_task_2_waiting():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-2-waiting.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            None,
            VisibleTask(2, TaskStatus.WAITING),
            VisibleTask(3, TaskStatus.READY),
            None,
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_tasks_waiting_during_date():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/date/tasks-waiting-during-date.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            None,
            VisibleTask(2, TaskStatus.READY),
            VisibleTask(3, TaskStatus.WAITING),
            VisibleTask(4, TaskStatus.WAITING),
            VisibleTask(5, TaskStatus.WAITING),
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


def test_task_1_waiting():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-1-waiting.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            VisibleTask(1, TaskStatus.WAITING),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()


@pytest.mark.skip(
    reason="The waiting status is not detected because of the smiley faces on top of it. Time before next read was "
    "increased to mitigate this."
)
def test_task_1_waiting2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-1-waiting2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.analyse_waiting_tasks(frame)

        assert frame.tasks == [
            VisibleTask(1, TaskStatus.WAITING),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

    finally:
        img_logger.finalize()
