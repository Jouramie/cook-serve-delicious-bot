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

        active_task = sensor.read_task_statement(img)
        assert active_task is None

    finally:
        img_logger.finalize()


def test_il():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/il.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task is None

    finally:
        img_logger.finalize()


def test_sc_oat_be():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/sc_oat_be.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task is None

    finally:
        img_logger.finalize()


def test_the_ryan_davis_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_ryan_davis_2.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "The Ryan Davis"
        assert active_task.description == "Meat, Bacon, Cheese (2x) and Tomatoes"

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_triple_w_bacon_1.tiff"), cv2.COLOR_BGR2RGB)

        sensor.find_waiting_tasks(img)

        active_task = sensor.read_task_statement(img)
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

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "The Double"
        assert active_task.description == "Meat (2x), Lettuce, Bacon, Cheese and Tomatoes"

    finally:
        img_logger.finalize()


def test_medium_cola():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-cola.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "Medium Cola"
        assert active_task.description == "A Medium Cola with Ice, please."

    finally:
        img_logger.finalize()


def test_medium_grape_w_flavor_blast():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-grape-w-flavor-blast.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "Medium Grape w/Flavor Blast"
        assert active_task.description == "A Medium Grape with Ice and Flavor Blast, please."

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_1.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "The Triple w/Bacon"
        assert active_task.description == "Meat (3x), Bacon and Cheese"

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_2.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "The Triple w/Bacon"
        assert active_task.description == "Meat (3x), Bacon and Cheese"

    finally:
        img_logger.finalize()


def test_nutty_chocolate():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/nutty_chocolate.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "Nutty Chocolate"
        assert active_task.description == "Two Chocolate Scoops and Nuts"

    finally:
        img_logger.finalize()


def test_the_yin_and_yang():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/the_yin_and_yang.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "The Yin and Yang"
        assert active_task.description == "One Vanilla, One Chocolate, Cherry and Sprinkles"

    finally:
        img_logger.finalize()


def test_trio_of_delicious():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/trio_of_delicious.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "Trio of Delicious"
        assert active_task.description == "One Vanilla, One Chocolate and One Mint Chocolate Chip, please."

    finally:
        img_logger.finalize()


def test_nutty_vanilla():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/nutty_vanilla.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "Nutty Vanilla"
        assert active_task.description == "Two Vanilla Scoops with Nuts"

    finally:
        img_logger.finalize()


def test_cherry_vanilla():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/cherry_vanilla.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img)
        assert active_task.title == "Cherry Vanilla"
        assert active_task.description == "Two Vanilla Scoops with a Cherry, please."

    finally:
        img_logger.finalize()


def test_red_deluxe_pasta():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/red_deluxe_pasta.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img, log_steps="red_deluxe_pasta")
        assert active_task.title == "Red Deluxe Pasta"
        assert (
            active_task.description
            == "Red Sauce, Meatballs, Chicken, Bacon, Red Peppers, Mushrooms, Spinach and Onions"
        )

    finally:
        img_logger.finalize()


def test_robbery():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/robbery.tiff"), cv2.COLOR_BGR2RGB)

        active_task = sensor.read_task_statement(img, log_steps="robbery")
        assert active_task.title == "Robbery (Witness Criminal Description)"
        assert (
            "He looked crazy! Crazy eyes, but bald and normal ears/nose, long lips and a beard."
            in active_task.description
        )

    finally:
        img_logger.finalize()
