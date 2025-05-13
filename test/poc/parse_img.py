import cv2

from core import sensor
from kit_test import img_logger

if __name__ == "__main__":
    try:
        imgs = [
            cv2.imread(r"logs/2023-09-06T233349.139947.tiff"),
        ]
        for img in imgs:
            print(img.shape)
            waiting_tasks = sensor.find_waiting_tasks(img)
            print(f"{waiting_tasks} are waiting")

            active_task = sensor.read_task_statement(img)
            print(f"Active task is {active_task.title}: {active_task.description}")
    finally:
        img_logger.finalize()
