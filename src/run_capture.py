import logging
import time
from pathlib import Path

import properties
from core import motor
from kit import img_logger, sensor_util


def loop():
    img_logger.submit(camera.capture_now())
    img_logger.publish()
    time.sleep(0.5)


if __name__ == "__main__":
    camera = None
    try:
        logs_folder = Path("logs")
        if not logs_folder.exists():
            logs_folder.mkdir()

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            handlers=[logging.FileHandler("logs/capture.log", mode="w")],
        )
        logger = logging.getLogger(__name__)

        camera = sensor_util.create_camera(properties.GAME_WINDOW_TITLE)

        img_logger.start()
        camera = sensor_util.create_camera(properties.GAME_WINDOW_TITLE)
        camera.start()

        motor.wait_for_game_to_start()
        while True:
            loop()
    finally:
        camera.stop()
        img_logger.finalize()
