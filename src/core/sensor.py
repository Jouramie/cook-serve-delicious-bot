import logging
import re
from dataclasses import dataclass, field

import cv2
import numpy as np
from numpy import float64
from pytesseract import pytesseract

from botkit import sensor_util, img_logger
from botkit.profiling import timeit
from core.brain import TaskStatement, VisibleTask, TaskStatus

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

STATUS_TASK_1_REGION = sensor_util.Region.of_corners(216, 85, 242, 116)
STATUS_TASK_2_REGION = sensor_util.Region.of_corners(216, 144, 242, 175)
STATUS_TASK_3_REGION = sensor_util.Region.of_corners(216, 203, 242, 234)
STATUS_TASK_4_REGION = sensor_util.Region.of_corners(216, 262, 242, 293)
STATUS_TASK_5_REGION = sensor_util.Region.of_corners(216, 321, 242, 352)
STATUS_TASK_6_REGION = sensor_util.Region.of_corners(216, 380, 242, 411)
STATUS_TASK_7_REGION = sensor_util.Region.of_corners(216, 439, 242, 470)
STATUS_TASK_8_REGION = sensor_util.Region.of_corners(216, 498, 242, 529)
STATUS_TASK_REGIONS = [
    STATUS_TASK_1_REGION,
    STATUS_TASK_2_REGION,
    STATUS_TASK_3_REGION,
    STATUS_TASK_4_REGION,
    STATUS_TASK_5_REGION,
    STATUS_TASK_6_REGION,
    STATUS_TASK_7_REGION,
    STATUS_TASK_8_REGION,
]
STATUS_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 25]), np.array([255, 100, 160]))

CURRENT_STATEMENT_REGION = sensor_util.Region.of_corners(270, 562, 1035, 677)
CURRENT_STATEMENT_MASK_1 = sensor_util.HsvColorBoundary(np.array([0, 0, 0]), np.array([255, 255, 20]))
CURRENT_STATEMENT_MASK_2 = sensor_util.HsvColorBoundary(np.array([0, 20, 0]), np.array([255, 40, 94]))

TITLE_PATTERN = re.compile(r"(\w[\w\s()/\-.&]+)")
DESCRIPTION_PATTERN = re.compile(r".+")


class NoStatementFoundException(Exception):
    pass


@dataclass
class Frame:
    img: np.ndarray = field(repr=False)

    tasks: list[VisibleTask | None] | None = None
    current_statement: TaskStatement | None = None

    _rush_overlay_ratio: float64 | None = None

    @property
    def has_found_tasks(self) -> bool:
        return bool(self.tasks)

    @property
    def current_statement_title(self) -> str | None:
        if self.current_statement is None:
            return None
        return self.current_statement.title

    def fix_rush_overlay_greyscale(self, img: np.ndarray) -> np.ndarray:
        if self._rush_overlay_ratio is None:
            self._detect_rush_overlay_strength()

        if self._rush_overlay_ratio:
            return (255 - (255 - img) / self._rush_overlay_ratio).astype(np.uint8)
        return img

    def _detect_rush_overlay_strength(self) -> None:
        waiting_task_background_color = self.img[WAITING_TASK_1_REGION.top, WAITING_TASK_1_REGION.left, 0]
        actual_waiting_task_background_darkness = np.array([255], dtype=np.uint8) - waiting_task_background_color
        self._rush_overlay_ratio = actual_waiting_task_background_darkness / EXPECTED_WAITING_TASK_BACKGROUND_DARKNESS

        if self._rush_overlay_ratio <= 1.0:
            logger.info(f"Rush hour detected. Overlay strength: {1 - self._rush_overlay_ratio}")


@timeit(name="analyse_waiting_tasks", print_each_call=True)
def analyse_waiting_tasks(frame: Frame, log_steps="") -> None:
    frame.tasks = [None, None, None, None, None, None, None, None]

    for i, region in enumerate(WAITING_TASK_REGIONS):
        task_number = i + 1
        cropped_task = sensor_util.crop(frame.img, region)
        if np.any(cropped_task[0, 0] != cropped_task[0, 0].flat[0]):
            logger.debug(f"Task {task_number} is not present.")
            continue

        cropped_task = frame.fix_rush_overlay_greyscale(cropped_task)
        if log_steps:
            img_logger.log_now(cropped_task, f"{log_steps}_{task_number}_cropped.tiff")

        masked_active = sensor_util.mask(cropped_task, WAITING_TASK_MASK)
        masked_blink = sensor_util.mask(cropped_task, WAITING_TASK_BLINK_MASK)
        masked = np.add(masked_active, masked_blink)
        if log_steps:
            img_logger.log_now(masked, f"{log_steps}_{task_number}_masked.tiff")
        if not (np.sum(masked) > 255 * 100):
            continue

        frame.tasks[i] = VisibleTask(task_number, find_task_status(frame, i, log_steps=log_steps))


def find_task_status(frame: Frame, i: int, log_steps="") -> TaskStatus:
    cropped_status = sensor_util.crop(frame.img, STATUS_TASK_REGIONS[i])
    cropped_status = frame.fix_rush_overlay_greyscale(cropped_status)

    if log_steps:
        img_logger.log_now(cropped_status, f"{log_steps}_{i+1}_status_cropped.tiff")

    masked = sensor_util.mask(cropped_status, STATUS_TASK_MASK)
    if log_steps:
        img_logger.log_now(masked, f"{log_steps}_{i+1}_status_masked.tiff")

    circles = cv2.HoughCircles(
        masked, cv2.HOUGH_GRADIENT, dp=1, minDist=10, param1=10, param2=10, minRadius=8, maxRadius=11
    )

    if circles is None:
        return TaskStatus.READY

    if log_steps:
        circles = np.uint16(np.around(circles))
        j = circles[0, :][0]
        cv2.circle(cropped_status, (j[0], j[1]), j[2], (0, 255, 0), 1)
        cv2.circle(cropped_status, (j[0], j[1]), 2, (0, 0, 255), 1)
        img_logger.log_now(cropped_status, f"{log_steps}_{i}_circle_{j}.tiff")

    return TaskStatus.WAITING


@timeit(name="read_task_statement", print_each_call=True)
def read_task_statement(frame: Frame, log_steps="") -> None:
    cropped = sensor_util.crop(frame.img, CURRENT_STATEMENT_REGION)
    cropped = frame.fix_rush_overlay_greyscale(cropped)

    if log_steps:
        img_logger.log_now(cropped, log_steps + "_cropped.png")
    masked_1 = sensor_util.mask(cropped, CURRENT_STATEMENT_MASK_1)
    masked_2 = sensor_util.mask(cropped, CURRENT_STATEMENT_MASK_2)
    masked = np.logical_or(masked_1, masked_2)
    if log_steps:
        img_logger.log_now(masked_1, log_steps + "_masked1.png")
        img_logger.log_now(masked_2, log_steps + "_masked2.png")
        img_logger.log_now(masked, log_steps + "_masked.png")

    # Statement mask finds white text on a black background, so if there is too much white, we assume
    # that there is no task statement.
    if np.sum(masked) > 255 * 20000:
        logger.warning("No task statement found.")
        return

    statement: str | None = pytesseract.image_to_string(masked, lang="eng")
    logger.info(f"Extracted `{statement}` from image.")
    if not statement:
        return

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
        return

    frame.current_statement = TaskStatement(title, description)
