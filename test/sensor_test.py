import cv2

from core import sensor
from kit import img_logger


def test_ee_8():
    try:
        img = cv2.imread(r"resources/ghost_tasks/ee_8.tiff")

        active_task = sensor.read_task_statement(img)
        assert active_task is None

    finally:
        img_logger.finalize()


def test_ree():
    try:
        img = cv2.imread(r"resources/ghost_tasks/ree.tiff")

        active_task = sensor.read_task_statement(img)
        assert active_task is None

    finally:
        img_logger.finalize()


def test_il():
    try:
        img = cv2.imread(r"resources/ghost_tasks/il.tiff")

        active_task = sensor.read_task_statement(img)
        assert active_task is None

    finally:
        img_logger.finalize()


def test_the_ryan_davis_2():
    try:
        img = cv2.imread(r"resources/burger/the_ryan_davis_2.tiff")

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "The Ryan Davis"
        assert active_task.description == "Meat, Bacon, Cheese (2x) and Tomatoes"

    finally:
        img_logger.finalize()


def test_the_triple_2():
    try:
        img = cv2.imread(r"resources/burger/the_triple_2.tiff")

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "The Triple"
        assert active_task.description == "Meat (3x) and Cheese"

    finally:
        img_logger.finalize()
