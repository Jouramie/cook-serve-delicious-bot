import cv2

from core import sensor
from kit import img_logger


def test_ee_8():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/ee_8.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img, log_steps="ee_8")
        assert active_task is None

    finally:
        img_logger.finalize()


def test_ree():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/ree.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img, log_steps="ree")
        assert active_task is None

    finally:
        img_logger.finalize()


def test_il():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/il.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img, log_steps="il")
        assert active_task is None

    finally:
        img_logger.finalize()


def test_the_ryan_davis_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_ryan_davis_2.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img, log_steps="the_ryan_davis_2")
        assert active_task.title == "The Ryan Davis"
        assert active_task.description == "Meat, Bacon, Cheese (2x) and Tomatoes"

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_triple_w_bacon_1.tiff"), cv2.COLOR_BGR2RGB)

        sensor.find_waiting_tasks(img)

        active_task = sensor.read_task_statement(img, log_steps="the_triple_w_bacon_1")
        assert active_task.title == "The Triple w/Bacon"
        assert active_task.description == "Three meat patties..."

    finally:
        img_logger.finalize()


def test_the_triple_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_triple_2.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "The Triple"
        assert active_task.description == "Meat (3x) and Cheese"

    finally:
        img_logger.finalize()


def test_the_double_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_double_2.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img, log_steps="the_double_2")
        assert active_task.title == "The Double"
        assert active_task.description == "Meat (2x), Lettuce, Bacon, Cheese and Tomatoes"

    finally:
        img_logger.finalize()


def test_medium_cola():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium_cola.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img, log_steps="medium_cola")
        assert active_task.title == "Medium Cola"
        assert active_task.description == "A Medium Cola with Ice, please."

    finally:
        img_logger.finalize()
