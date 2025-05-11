import cv2

from core import sensor
from kit import img_logger


def test_ee_8():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/ee_8.tiff"), cv2.COLOR_BGR2RGB)

        hour = sensor.read_hour(img, log_steps="ee_8")
        assert hour == "1204" or hour is None

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_triple_w_bacon_1.tiff"), cv2.COLOR_BGR2RGB)

        sensor.find_waiting_tasks(img)

        hour = sensor.read_hour(img, log_steps="the_triple_w_bacon_1")
        assert hour == "924" or hour is None

    finally:
        img_logger.finalize()


def test_medium_grape_w_flavor_blast():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-grape-w-flavor-blast.tiff"), cv2.COLOR_BGR2RGB)

        hour = sensor.read_hour(img, log_steps="medium_grape_w_flavor_blast")
        assert hour == "643" or hour is None

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_1.tiff"), cv2.COLOR_BGR2RGB)

        hour = sensor.read_hour(img, log_steps="the_triple_w_bacon_2_rush_hour_1")
        assert hour == "102"

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_2.tiff"), cv2.COLOR_BGR2RGB)

        hour = sensor.read_hour(img, log_steps="the_triple_w_bacon_2_rush_hour_2")
        assert hour == "101"

    finally:
        img_logger.finalize()
