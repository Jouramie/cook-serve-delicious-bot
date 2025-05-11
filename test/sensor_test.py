import cv2

from core import sensor
from kit import img_logger


def test_ee_8():
    try:
        img = cv2.imread(r"resources/ee_8.tiff")

        waiting_tasks = sensor.find_waiting_tasks(img)
        assert waiting_tasks == [2]

        active_task = sensor.read_task_statement(img)
        assert active_task is None

    finally:
        img_logger.finalize()
