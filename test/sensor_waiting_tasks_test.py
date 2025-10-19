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

        tasks = sensor.find_waiting_tasks(img)
        assert tasks == [2, 3, 4]

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_1.tiff"), cv2.COLOR_BGR2RGB)

        tasks = sensor.find_waiting_tasks(img)
        assert tasks == [1, 2, 3]

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_2.tiff"), cv2.COLOR_BGR2RGB)

        tasks = sensor.find_waiting_tasks(img)
        assert tasks == [1, 2, 3]

    finally:
        img_logger.finalize()


def test_task_2_blink_rush_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-2-blink-rush-1.tiff"), cv2.COLOR_BGR2RGB)

        tasks = sensor.find_waiting_tasks(img)
        assert tasks == [1, 2]

    finally:
        img_logger.finalize()


def test_task_2_blink_rush_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/task-2-blink-rush-2.tiff"), cv2.COLOR_BGR2RGB)

        tasks = sensor.find_waiting_tasks(img)
        assert tasks == [1, 2]

    finally:
        img_logger.finalize()


def test_5_tasks():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/5-tasks.tiff"), cv2.COLOR_BGR2RGB)

        tasks = sensor.find_waiting_tasks(img)
        assert tasks == [1, 3, 5]

    finally:
        img_logger.finalize()
