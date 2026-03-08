import json
import logging
import time
from importlib.resources import files

import numpy as np

import properties
from botkit import img_logger, sensor_util
from botkit.profiling import timeit
from botkit.sensor_util import create_camera
from core import motor, sensor, brain, resources, menu_optimization
from core.menu_optimization import MenuOption, Booster, Detractor

logger = logging.getLogger(__name__)


def run_capture() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler("logs/capture.log", mode="w")],
    )

    def loop() -> None:
        img_logger.submit(camera.capture_now())
        img_logger.publish()
        time.sleep(0.5)

    camera = None
    try:
        img_logger.start()
        camera = sensor_util.create_camera(properties.GAME_WINDOW_TITLE)
        camera.start()

        motor.wait_for_game_to_start()
        while True:
            loop()

    finally:
        camera.stop()
        img_logger.finalize()


def run_bot() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler("logs/bot.log", mode="w")],
    )

    def capture() -> np.ndarray:
        frame = camera.get_latest_frame()
        img_logger.submit(frame)
        img_logger.publish()
        return frame

    @timeit(name="loop", print_each_call=True)
    def loop() -> None:
        """
        1. Find and store new active tasks
            - Store timestamps on when it was detected
        2. Execute tasks
            - Read title, find known task in dictionary
            -
        """

        last_frame = sensor.Frame(capture())
        sensor.analyse_waiting_tasks(last_frame)
        if not last_frame.has_found_tasks:
            logger.info(f"Found no waiting tasks.")
            return

        task, task_callback = brain.choose_task_to_execute(last_frame.tasks)
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

            statement_retry = 0
            while last_frame.current_statement is None:
                last_frame = sensor.Frame(capture())
                sensor.analyse_waiting_tasks(last_frame)
                sensor.read_task_statement(last_frame)

                if last_frame.current_statement is None:
                    statement_retry += 1
                    if statement_retry >= 3:
                        logger.warning(f"No statement after 3 tries, will choose another task.")
                        return
                    logger.info(f"Waiting for statement to appear...")

            logger.info(f"Found statement {last_frame.current_statement}")
            task_execution = task_callback(last_frame.tasks, last_frame.current_statement)
            if task_execution.is_unknown:
                execution_retry += 1
                if execution_retry >= 3:
                    logger.warning(
                        f"Could not find a proper execution for task {last_frame.current_statement_title}, but will execute anyway."
                    )
                    break

                logger.warning(
                    f"Could not find a proper execution for task {last_frame.current_statement_title}. Will retry reading statement."
                )
                task_execution = None

        motor.execute_task(task_execution)
        camera.flush()

    camera = None
    try:
        img_logger.start()
        camera = create_camera(properties.GAME_WINDOW_TITLE)
        camera.start()

        motor.wait_for_game_to_start()
        while True:
            loop()

    finally:
        if camera is not None:
            camera.stop()
        img_logger.finalize()
        time.sleep(1)


def optimize_menu() -> None:
    menu_items: dict[str, MenuOption] = {}

    with files(resources).joinpath("foods.json").open() as foods_file:
        for k, v in json.load(foods_file).items():
            menu_items[k] = MenuOption(
                k,
                v["prices_per_star"],
                {Booster(b) for b in v["boosters"]},
                {Detractor(d) for d in v["detractors"]},
            )

    best_menu = menu_optimization.choose_best_menu(
        menu_items,
        properties.UNLOCKED_FOOD_LEVELS,
        properties.CURRENT_RESTAURANT_STARS,
        properties.MENU_ROT,
        properties.MANDATORY_FOOD,
        properties.RAINING_HOURS,
        properties.AVAILABLE_PURCHASES,
        properties.UPGRADE_BUDGET,
    )

    print(best_menu)


def advise_purchases() -> None:
    menu_items: list[MenuOption] = []

    with files(resources).joinpath("foods.json").open() as foods_file:
        for k, v in json.load(foods_file).items():
            menu_items.append(
                MenuOption(
                    k,
                    v["prices_per_star"],
                    {Booster(b) for b in v["boosters"]},
                    {Detractor(d) for d in v["detractors"]},
                )
            )

    advised_purchases = menu_optimization.advise_purchases(
        menu_items,
        properties.UPGRADE_BUDGET,
        properties.AVAILABLE_PURCHASES,
        properties.UNLOCKED_FOOD_LEVELS,
    )
    print(advised_purchases)
