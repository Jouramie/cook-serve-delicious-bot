import logging

import numpy as np
from pytesseract import pytesseract

from core.brain import TaskStatement
from kit import sensor_util
from kit.profiling import timeit

logger = logging.getLogger(__name__)

WAITING_TASKS_REGION = sensor_util.Region.of_corners(0, 75, 50, 305)
WAITING_TASK_1_REGION = sensor_util.Region.of_corners(0, 75, 50, 125)
WAITING_TASK_2_REGION = sensor_util.Region.of_corners(0, 135, 50, 185)
WAITING_TASK_3_REGION = sensor_util.Region.of_corners(0, 195, 50, 245)
WAITING_TASK_4_REGION = sensor_util.Region.of_corners(0, 255, 50, 305)
WAITING_TASK_REGIONS = [WAITING_TASK_1_REGION, WAITING_TASK_2_REGION, WAITING_TASK_3_REGION, WAITING_TASK_4_REGION]
WAITING_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 240]), np.array([5, 5, 255]))

ACTIVE_TASK_REGION = sensor_util.Region.of_corners(270, 562, 1035, 677)
ACTIVE_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 0]), np.array([255, 255, 85]))


def remove_quotes(txt):
    for q in ['"', "'", "”"]:
        txt = txt.replace(q, "")
    return txt


class NoStatementFoundException(Exception):
    pass


@timeit(name="find_waiting_tasks", print_each_call=True)
def find_waiting_tasks(img: np.ndarray) -> list[int]:
    tasks = []
    for i, region in enumerate(WAITING_TASK_REGIONS):
        cropped_task = sensor_util.crop(img, region)
        masked = sensor_util.mask(cropped_task, WAITING_TASK_MASK)
        # img_logger.log_now(masked, f"cropped{i}.png")
        if masked.any():
            tasks.append(1 + i)
    return tasks


@timeit(name="read_task_statement", print_each_call=True)
def read_task_statement(img: np.ndarray) -> TaskStatement | None:
    cropped = sensor_util.crop(img, ACTIVE_TASK_REGION)
    masked = sensor_util.mask(cropped, ACTIVE_TASK_MASK)
    statement: str | None = pytesseract.image_to_string(masked)
    logger.info(f"Extracted `{statement}` from image.")
    if not statement:
        return None

    statement_split = statement.split("\n")
    title, description = statement_split[0], statement_split[2]
    title = remove_quotes(title)
    return TaskStatement(title, description)
