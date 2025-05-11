import logging
import sys
from datetime import datetime

import cv2

from core import sensor
from core.brain import StatementCallback, Task
from kit import img_logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        imgs = [
            cv2.imread(r"logs/2025-05-10T152110.037598.tiff"),
        ]
        for img in imgs:
            logger.info(f"Image shape if {img.shape}")
            waiting_tasks = sensor.find_waiting_tasks(img)
            logger.info(f"{waiting_tasks} are waiting")
            task = Task(waiting_tasks[0], datetime.now())
            callback = StatementCallback(task)

            active_statement = sensor.read_task_statement(img, log_steps=True)
            logger.info(f"Active task is {active_statement.title}: {active_statement.description}")

            if active_statement is None:
                logger.warning("No active task found.")
                continue

            instructions = callback(waiting_tasks, active_statement)

    finally:
        img_logger.finalize()
