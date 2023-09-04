import logging
from pathlib import Path

import properties
from core import sensor, brain, motor
from kit import img_logger, sensor_util
from kit.profiling import timeit


def capture():
    frame = camera.get_latest_frame()
    img_logger.submit(frame)
    img_logger.publish()
    return frame


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
    if not waiting_tasks:
        logger.info(f"Found no waiting tasks.")
        return

    logger.info(f"Tasks {waiting_tasks} are waiting.")
    task, instruction_callback = brain.choose_task_to_execute(waiting_tasks)
    logger.info(f"Executing on task {task}")
    motor.select_task(task)

    camera.flush()
    statement = None
    while statement is None:
        last_frame = capture()
        waiting_tasks = sensor.find_waiting_tasks(last_frame)
        statement = sensor.read_task_statement(last_frame)
        if statement is None:
            logger.info(f"Waiting for statement to appear...")
    logger.info(f"Found statement {statement}")
    instruction = instruction_callback(waiting_tasks, statement)
    motor.execute_instruction(instruction)


if __name__ == "__main__":
    try:
        logs_folder = Path("logs")
        if not logs_folder.exists():
            logs_folder.mkdir()

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            handlers=[(logging.FileHandler("logs/bot.log", mode="w"))],
        )
        logger = logging.getLogger(__name__)

        img_logger.start()
        camera = sensor_util.create_camera(properties.GAME_WINDOW_TITLE)
        camera.start()

        motor.wait_for_game_to_start()
        while True:
            loop()
    finally:
        camera.stop()
        img_logger.finalize()
