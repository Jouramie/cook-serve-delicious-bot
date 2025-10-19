import logging
from pathlib import Path
from time import sleep

import properties
from core import sensor, brain, motor
from botkit import img_logger, sensor_util
from botkit.profiling import timeit


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

    task, task_callback = brain.choose_task_to_execute(waiting_tasks)
    if task_callback is None:
        return

    logger.info(f"Launching task {task}")

    if task_callback.is_executable:
        motor.execute_task(task_callback)
        camera.flush()
        return
    motor.select_task(task.index)
    camera.flush()

    task_execution = None
    execution_retry = 0
    while task_execution is None:
        statement = None
        statement_retry = 0
        while statement is None:
            last_frame = capture()
            waiting_tasks = sensor.find_waiting_tasks(last_frame)
            statement = sensor.read_task_statement(last_frame)
            if statement is None:
                statement_retry += 1
                if statement_retry >= 3:
                    logger.warning(f"No statement after 3 tries, will choose another task.")
                    return
                logger.info(f"Waiting for statement to appear...")

        logger.info(f"Found statement {statement}")
        task_execution = task_callback(waiting_tasks, statement)
        if task_execution.is_unknown:
            execution_retry += 1
            if execution_retry >= 3:
                logger.warning(
                    f"Could not find a proper execution for task {statement.title}, but will execute anyway."
                )
                break

            logger.warning(
                f"Could not find a proper execution for task {statement.title}. Will retry reading statement."
            )
            task_execution = None

    motor.execute_task(task_execution)
    camera.flush()


if __name__ == "__main__":
    try:
        logs_folder = Path("logs")
        if not logs_folder.exists():
            logs_folder.mkdir()

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            handlers=[logging.FileHandler("logs/bot.log", mode="w")],
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
        sleep(1)
