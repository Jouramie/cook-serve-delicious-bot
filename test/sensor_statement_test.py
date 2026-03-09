import cv2

from botkit import img_logger
from botkit.text import normalized_levenshtein_distance as nld
from core import sensor

OCR_ERROR_TOLERANCE = 0.95


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
        expected_statement = "Meat, Bacon, Cheese (2x) and Tomatoes"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_triple_w_bacon_1.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Triple w/Bacon"
        expected_statement = "Three meat patties..."
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_the_triple_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_triple_2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Triple"
        expected_statement = "Meat (3x) and Cheese"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_the_double_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/burger/the_double_2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Double"
        expected_statement = "Meat (2x), Lettuce, Bacon, Cheese and Tomatoes"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_medium_cola():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-cola.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Medium Cola"
        expected_statement = "A Medium Cola with Ice, please."
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_medium_grape_w_flavor_blast():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/medium-grape-w-flavor-blast.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Medium Grape w/Flavor Blast"
        expected_statement = "A Medium Grape with Ice and Flavor Blast, please."
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_1():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_1.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Triple w/Bacon"
        expected_statement = "Meat (3x), Bacon and Cheese"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_the_triple_w_bacon_2_rush_hour_2():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/the_triple_w_bacon_2_rush_hour_2.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Triple w/Bacon"
        expected_statement = "Meat (3x), Bacon and Cheese"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_nutty_chocolate():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/nutty_chocolate.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Nutty Chocolate"
        expected_statement = "Two Chocolate Scoops and Nuts"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_the_yin_and_yang():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/the_yin_and_yang.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "The Yin and Yang"
        expected_statement = "One Vanilla, One Chocolate, Cherry and Sprinkles"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_trio_of_delicious():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/trio_of_delicious.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Trio of Delicious"
        expected_statement = "One Vanilla, One Chocolate and One Mint Chocolate Chip, please."
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_nutty_vanilla():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/nutty_vanilla.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Nutty Vanilla"
        expected_statement = "Two Vanilla Scoops with Nuts"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_cherry_vanilla():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/ice_cream/cherry_vanilla.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Cherry Vanilla"
        expected_statement = "Two Vanilla Scoops with a Cherry, please."
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_red_deluxe_pasta():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/red_deluxe_pasta.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Red Deluxe Pasta"
        expected_statement = "Red Sauce, Meatballs, Chicken, Bacon, Red Peppers, Mushrooms, Spinach and Onions"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_robbery():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/robbery.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Robbery (Witness Criminal Description)"
        expected_statement = "He looked crazy! Crazy eyes, but bald and normal ears/nose, long lips and a beard. Gah!"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_tons():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/tons.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Mixed Delicious"
        expected_statement = "(2) Ebi, (3) Roe, (2) Toro, (1) Tuna"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_the_dishes():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/bot-dont-want-to-clean-the-dishes.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame)

        assert frame.current_statement.title == "Work Ticket (Dishes)"
        expected_statement = "The dishes need cleaning..."
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()


def test_chomper_plate():
    try:
        img = cv2.cvtColor(cv2.imread(r"resources/chomper-plate.tiff"), cv2.COLOR_BGR2RGB)
        frame = sensor.Frame(img)

        sensor.read_task_statement(frame, log_steps="chomper_plate")

        assert frame.current_statement.title == "Chomper Plate"
        expected_statement = "(1) Ebi, (3) Roe, (2) Tuna, (1) Salman, (1) Mackerel"
        assert nld(frame.current_statement.description, expected_statement) > OCR_ERROR_TOLERANCE

    finally:
        img_logger.finalize()
