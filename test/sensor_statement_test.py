import cv2

from botkit import img_logger
from core import sensor


def test_ee_8():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/ee_8.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement is None

    finally:
        img_logger.finalize()


def test_ree():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/ree.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement is None

    finally:
        img_logger.finalize()


def test_il():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/il.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement is None

    finally:
        img_logger.finalize()


def test_sc_oat_be():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ghost_tasks/sc_oat_be.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement is None

    finally:
        img_logger.finalize()


def test_the_ryan_davis_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_ryan_davis_2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Ryan Davis"
        assert frame.current_statement.description == "Meat, Bacon, Cheese (2x) and Tomatoes"

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_triple_w_bacon_1.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Triple w/Bacon"
        assert frame.current_statement.description == "Three meat patties..."

    finally:
        img_logger.finalize()


def test_the_triple_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_triple_2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Triple"
        assert frame.current_statement.description == "Meat (3x) and Cheese"

    finally:
        img_logger.finalize()


def test_the_double_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_double_2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Double"
        assert frame.current_statement.description == "Meat (2x), Lettuce, Bacon, Cheese and Tomatoes"

    finally:
        img_logger.finalize()


def test_medium_cola():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-cola.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Medium Cola"
        assert frame.current_statement.description == "A Medium Cola with Ice, please."

    finally:
        img_logger.finalize()


def test_medium_grape_w_flavor_blast():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-grape-w-flavor-blast.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Medium Grape w/Flavor Blast"
        assert frame.current_statement.description == "A Medium Grape with Ice and Flavor Blast, please."

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_1.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Triple w/Bacon"
        assert frame.current_statement.description == "Meat (3x), Bacon and Cheese"

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Triple w/Bacon"
        assert frame.current_statement.description == "Meat (3x), Bacon and Cheese"

    finally:
        img_logger.finalize()


def test_nutty_chocolate():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/nutty_chocolate.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Nutty Chocolate"
        assert frame.current_statement.description == "Two Chocolate Scoops and Nuts"

    finally:
        img_logger.finalize()


def test_the_yin_and_yang():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/the_yin_and_yang.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Yin and Yang"
        assert frame.current_statement.description == "One Vanilla, One Chocolate, Cherry and Sprinkles"

    finally:
        img_logger.finalize()


def test_trio_of_delicious():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/trio_of_delicious.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Trio of Delicious"
        assert frame.current_statement.description == "One Vanilla, One Chocolate and One Mint Chocolate Chip, please."

    finally:
        img_logger.finalize()


def test_nutty_vanilla():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/nutty_vanilla.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Nutty Vanilla"
        assert frame.current_statement.description == "Two Vanilla Scoops with Nuts"

    finally:
        img_logger.finalize()


def test_cherry_vanilla():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/cherry_vanilla.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Cherry Vanilla"
        assert frame.current_statement.description == "Two Vanilla Scoops with a Cherry, please."

    finally:
        img_logger.finalize()


def test_red_deluxe_pasta():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/red_deluxe_pasta.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Red Deluxe Pasta"
        assert (
            frame.current_statement.description
            == "Red Sauce, Meatballs, Chicken, Bacon, Red Peppers, Mushrooms, Spinach and Onions"
        )

    finally:
        img_logger.finalize()


def test_robbery():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/robbery.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Robbery (Witness Criminal Description)"
        assert (
            "He looked crazy! Crazy eyes, but bald and normal ears/nose, long lips and a beard."
            in frame.current_statement.description
        )

    finally:
        img_logger.finalize()
