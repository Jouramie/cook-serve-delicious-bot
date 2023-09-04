import logging
import time
from pathlib import Path

from util import img_logger, img_edit
from util.profiling import timeit

import properties
from core import sensor, brain, motor
from core.sensor import NoPlayerFoundException
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
    try:
        position, distance = sensor.detect_player()
        _detections_without_finding_player = 0
    except NoPlayerFoundException as e:
        logger.warning("I don't see the cursor !")
        sensor.clear()
        _detections_without_finding_player += 1
        if _detections_without_finding_player > properties.MAX_PLAYER_LOST:
            raise e
        motor.unstuck()
        sensor.clear()
        return
    available_distances = sensor.detect_available_distances()
    unsafe, direction = brain.choose_direction(position, distance, available_distances)
    motor.turn(unsafe, direction)

    img_logger.edit(img_edit.draw_player_rotation(position, direction, unsafe))
    img_logger.edit(img_edit.draw_safe_area(distance))
    img_logger.edit(img_edit.draw_unsafe_area(distance))

    sensor.clear()


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
