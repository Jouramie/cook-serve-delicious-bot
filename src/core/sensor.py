import logging

import numpy as np
from pytesseract import pytesseract

from core.model import TaskStatement
from kit import sensor_util
from kit.profiling import timeit

logger = logging.getLogger(__name__)

WAITING_TASKS_REGION = sensor_util.Region.of_corners(0, 150, 100, 610)
WAITING_TASK_1_REGION = sensor_util.Region.of_corners(0, 150, 100, 250)
WAITING_TASK_2_REGION = sensor_util.Region.of_corners(0, 270, 100, 370)
WAITING_TASK_3_REGION = sensor_util.Region.of_corners(0, 390, 100, 490)
WAITING_TASK_4_REGION = sensor_util.Region.of_corners(0, 510, 100, 610)
WAITING_TASK_REGIONS = [WAITING_TASK_1_REGION, WAITING_TASK_2_REGION, WAITING_TASK_3_REGION, WAITING_TASK_4_REGION]
WAITING_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 160]), np.array([255, 255, 255]))

ACTIVE_TASK_REGION = sensor_util.Region.of_corners(540, 1125, 2070, 1375)
ACTIVE_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 0]), np.array([255, 255, 85]))


class NoStatementFoundException(Exception):
    pass


@timeit(name="find_waiting_tasks", print_each_call=True)
def find_waiting_tasks(img: np.ndarray) -> list[int]:
    tasks = []
    for i, region in enumerate(WAITING_TASK_REGIONS):
        cropped_task = sensor_util.crop(img, region)
        masked = sensor_util.mask(cropped_task, WAITING_TASK_MASK)
        if masked.any():
            tasks.append(1 + i)
    return tasks


@timeit(name="read_task_statement", print_each_call=True)
def read_task_statement(img: np.ndarray) -> TaskStatement:
    cropped = sensor_util.crop(img, ACTIVE_TASK_REGION)
    masked = sensor_util.mask(cropped, ACTIVE_TASK_MASK)
    statement: str | None = pytesseract.image_to_string(masked)
    logger.info(f"Extracted `{statement}` from image.")
    if statement is None:
        raise NoStatementFoundException

    title, _, description = statement.split("\n")
    title = title.replace('"', "").replace("'", "")
    return TaskStatement(title, description)
