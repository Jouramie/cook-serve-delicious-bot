import logging
import time
from pathlib import Path

from util import img_logger
from util.profiling import timeit

import properties
from core import sensor, brain, motor
from kit import sensor_util


@timeit(name="capture", print_each_call=True)
def capture():
    camera.get_latest_frame()


@timeit(name="loop", print_each_call=True)
def loop():
    """
    1. Find and store new active tasks
        - Store timestamps on when it was detected
    2. Execute tasks
        - Read title, find known task in dictionary
        -
    """

    last_frame = capture()
    waiting_tasks = sensor.find_waiting_tasks(last_frame)
    task, callback = brain.choose_task_to_execute(waiting_tasks)
    motor.select_task(task)

    last_frame = capture()
    waiting_tasks = sensor.find_waiting_tasks(last_frame)
    statement = sensor.read_task_statement(last_frame)
    callback(waiting_tasks, statement)


if __name__ == "__main__":
    logs_folder = Path("logs")
    if not logs_folder.exists():
        logs_folder.mkdir()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[(logging.FileHandler("logs/bot.log", mode="w"))],
    )
    logger = logging.getLogger(__name__)

    camera = sensor_util.create_camera(properties.GAME_WINDOW_TITLE)

    print("Starting the bot in 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("Start !")
    try:
        while True:
            loop()
    finally:
        camera.stop()
        img_logger.finalize()
