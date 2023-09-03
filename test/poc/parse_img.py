from dataclasses import dataclass

import cv2
import numpy as np
import pytesseract

from kit import sensor_util, img_logger

WAITING_TASKS_REGION = sensor_util.Region(0, 150, 100, 610)
WAITING_TASK_1_REGION = sensor_util.Region(0, 150, 100, 250)
WAITING_TASK_2_REGION = sensor_util.Region(0, 270, 100, 370)
WAITING_TASK_3_REGION = sensor_util.Region(0, 390, 100, 490)
WAITING_TASK_4_REGION = sensor_util.Region(0, 510, 100, 610)
WAITING_TASK_REGIONS = [WAITING_TASK_1_REGION, WAITING_TASK_2_REGION, WAITING_TASK_3_REGION, WAITING_TASK_4_REGION]
WAITING_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 160]), np.array([255, 255, 255]))

ACTIVE_TASK_REGION = sensor_util.Region(540, 1125, 2070, 1375)
ACTIVE_TASK_MASK = sensor_util.HsvColorBoundary(np.array([0, 0, 0]), np.array([255, 255, 85]))


def find_waiting_tasks(img: np.ndarray):
    tasks = []
    for i, region in enumerate(WAITING_TASK_REGIONS):
        cropped_task = sensor_util.crop(img, region)
        masked = sensor_util.mask(cropped_task, WAITING_TASK_MASK)
        if masked.any():
            tasks.append(1 + i)
    return tasks


@dataclass
class Task:
    title: str
    description: str


def find_active_task(img: np.ndarray) -> Task:
    cropped = sensor_util.crop(img, ACTIVE_TASK_REGION)
    img_logger.log_now(cropped, "cropped.tiff")
    masked = sensor_util.mask(cropped, ACTIVE_TASK_MASK)
    img_logger.log_now(masked, "masked.tiff")
    txt = pytesseract.image_to_string(masked)
    print(txt)


if __name__ == "__main__":
    try:
        imgs = [
            cv2.imread(r"test/resources/grey-tail-fish.png"),
            cv2.imread(r"test/resources/cherry-vanilla-while-salad-waiting.png"),
            cv2.imread(r"test/resources/the-manhattan.png"),
        ]
        for img in imgs:
            print(img.shape)
            active_task = find_active_task(img)
            waiting_tasks = find_waiting_tasks(img)

            print(f"Active task is {active_task.title}: {active_task.description }")
            print(f"{waiting_tasks} are waiting")
    finally:
        img_logger.finalize()
