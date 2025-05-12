import cv2

from core import sensor
from kit import img_logger


def test_medium_grape_w_flavor_blast():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-grape-w-flavor-blast.tiff"), cv2.COLOR_BGR2RGB)

        tasks = sensor.find_waiting_tasks(img, "medium_grape_w_flavor_blast")
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
