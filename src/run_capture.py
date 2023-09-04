import logging
import time
from pathlib import Path

import properties
from kit import img_logger, sensor_util


def loop():
    img_logger.log_now(camera.capture_now())
    time.sleep(0.1)


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

        print("Starting the capture in 3...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)
        print("Start !")

        while True:
            loop()
    finally:
        if camera is not None:
            camera.stop()
        img_logger.finalize()
