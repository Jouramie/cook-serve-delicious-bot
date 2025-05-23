import logging
import re

import numpy as np
from pytesseract import pytesseract

from core.brain import TaskStatement
from kit import sensor_util, img_logger
from kit.profiling import timeit

logger = logging.getLogger(__name__)

WAITING_TASK_1_REGION = sensor_util.Region.of_corners(0, 75, 50, 125)
WAITING_TASK_2_REGION = sensor_util.Region.of_corners(0, 135, 50, 185)
WAITING_TASK_3_REGION = sensor_util.Region.of_corners(0, 195, 50, 245)
WAITING_TASK_4_REGION = sensor_util.Region.of_corners(0, 255, 50, 305)
WAITING_TASK_5_REGION = sensor_util.Region.of_corners(0, 315, 50, 365)
WAITING_TASK_6_REGION = sensor_util.Region.of_corners(0, 375, 50, 425)
WAITING_TASK_7_REGION = sensor_util.Region.of_corners(0, 435, 50, 485)
WAITING_TASK_8_REGION = sensor_util.Region.of_corners(0, 495, 50, 545)
WAITING_TASK_REGIONS = [
    WAITING_TASK_1_REGION,
    WAITING_TASK_2_REGION,
    WAITING_TASK_3_REGION,
    WAITING_TASK_4_REGION,
    WAITING_TASK_5_REGION,
    WAITING_TASK_6_REGION,
    WAITING_TASK_7_REGION,
    WAITING_TASK_8_REGION,
]
WAITING_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 250]), np.array([5, 5, 255]))
WAITING_TASK_BLINK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 49]), np.array([5, 5, 51]))
EXPECTED_WAITING_TASK_BACKGROUND_DARKNESS = np.array([255], dtype=np.uint8) - np.array([28], dtype=np.uint8)

ACTIVE_TASK_REGION = sensor_util.Region.of_corners(270, 562, 1035, 677)
ACTIVE_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 0]), np.array([255, 255, 171]))
RUSH_HOUR_ACTIVE_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 220]), np.array([255, 255, 255]))

HOUR_REGION = sensor_util.Region.of_corners(1180, 3, 1278, 40)
HOUR_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 220]), np.array([255, 255, 255]))
RUSH_HOURS = {"100", "101", "102", "103", "104", "105"}

TITLE_PATTERN = re.compile(r"(\w[\w\s()/\-.]+)")
DESCRIPTION_PATTERN = re.compile(r"\w.+")


class NoStatementFoundException(Exception):
    pass


@timeit(name="find_waiting_tasks", print_each_call=True)
def find_waiting_tasks(img: np.ndarray, log_steps="") -> list[int]:
    tasks = []

    waiting_task_background_color = img[WAITING_TASK_1_REGION.top, WAITING_TASK_1_REGION.left, 0]
    actual_waiting_task_background_darkness = np.array([255], dtype=np.uint8) - waiting_task_background_color
    rush_overlay_ratio = actual_waiting_task_background_darkness / EXPECTED_WAITING_TASK_BACKGROUND_DARKNESS
    rush_overlay_strength = 1 - rush_overlay_ratio
    if rush_overlay_strength:
        logger.info(f"Rush hour detected. Overlay strength: {rush_overlay_strength}")

    for i, region in enumerate(WAITING_TASK_REGIONS):
        cropped_task = sensor_util.crop(img, region)
        if np.any(cropped_task[0, 0] != cropped_task[0, 0].flat[0]):
            logger.debug(f"Task {i} is not present.")
            continue

        if rush_overlay_strength:
            cropped_task = (255 - (255 - cropped_task) / rush_overlay_ratio).astype(np.uint8)

        if log_steps:
            img_logger.log_now(cropped_task, f"{log_steps}_{i}_cropped.tiff")
        masked_active = sensor_util.mask(cropped_task, WAITING_TASK_MASK)
        masked_blink = sensor_util.mask(cropped_task, WAITING_TASK_BLINK_MASK)
        masked = np.add(masked_active, masked_blink)
        if log_steps:
            img_logger.log_now(masked, f"{log_steps}_{i}_masked.tiff")
        if np.sum(masked) > 255 * 100:
            tasks.append(1 + i)
    return tasks


@timeit(name="is_in_rush_hour", print_each_call=True)
def is_in_rush_hour(img: np.ndarray, log_steps="") -> bool:
    hour = read_hour(img, log_steps)
    if hour in RUSH_HOURS:
        return True
    return False


def read_hour(img, log_steps):
    cropped = sensor_util.crop(img, HOUR_REGION)
    masked = sensor_util.mask(cropped, HOUR_MASK)
    hour: str | None = pytesseract.image_to_string(masked, lang="fra", config="--psm 8")
    if hour is None:
        return None
    sanitized_hour = "".join(c for c in hour if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    if not sanitized_hour:
        return None
    return sanitized_hour


@timeit(name="read_task_statement", print_each_call=True)
def read_task_statement(img: np.ndarray, log_steps="") -> TaskStatement | None:
    cropped = sensor_util.crop(img, ACTIVE_TASK_REGION)
    masked = sensor_util.mask(cropped, ACTIVE_TASK_MASK)
    if log_steps:
        img_logger.log_now(masked, log_steps + "_masked.png")

    # Statement mask finds white text on a black background, so if there is too much white, we assume
    # that there is no task statement.
    if np.sum(masked) > 255 * 20000:
        logger.warning("No task statement found.")
        return None

    statement: str | None = pytesseract.image_to_string(masked, lang="eng")
    logger.info(f"Extracted `{statement}` from image.")
    if not statement:
        return None

    statement_split = statement.split("\n")
    title = description = None
    for txt in statement_split:
        if title is None:
            match = TITLE_PATTERN.search(txt)
            if match is not None:
                title = match.group()
                continue
        else:
            match = DESCRIPTION_PATTERN.match(txt)
            if match is not None:
                if description is None:
                    description = txt
                    continue

                description += " " + txt
                continue

    if title is None or description is None:
        return None

    return TaskStatement(title, description)
