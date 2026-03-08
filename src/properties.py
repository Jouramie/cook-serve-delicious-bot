import sys

# Sensor
if sys.platform == "darwin":
    GAME_WINDOW_TITLE = "Cook Serve Delicious"
    GAME_WINDOW_MARGIN = (1, 29, 1, 1)
elif sys.platform == "win32":
    GAME_WINDOW_TITLE = "Cook, Serve, Delicious!"
    GAME_WINDOW_MARGIN = (12, 46, 12, 13)


SCREENSHOT_LOGGER_LOGS_PATH = "logs"
SCREENSHOT_LOGGER_ENABLED = True
SCREENSHOT_LOGGER_IMAGE_NAME: None | str = None
SCREENSHOT_LOGGER_ROLLING_IMAGE_AMOUNT = 100
SCREENSHOT_LOGGER_EDIT_ENABLED = True


# Restaurant
CURRENT_RESTAURANT_STARS = 2
UNLOCKED_FOOD_LEVELS = {
    "Sopapillas": 1,
    "Corn Dog": 1,
    "Pretzel": 1,
    "Cold Beer": 1,
    "Fried Chicken": 2,
    "Soda Fountain": 2,
    "French Fries": 1,
    "Salad": 3,
    "Ice Cream": 3,
    "Baked Potato": 3,
    "Nachos": 1,
    "Lasagna": 2,
    "Fresh Fish": 3,
    "Chicken Breast": 4,
    "Pasta": 4,
    "Wine": 1,
    "Pizza": 3,
    "Burger": 3,
    "Steak": 3,
    "Soups": 3,
    "Coffee": 2,
    "Hash Browns": 0,
    "Breakfast Sandwich": 0,
    "Pancakes": 0,
    "Sushi": 1,
    "Fried Rice": 0,
    "Lobster": 0,
    "Banana Foster": 0,
    "Shish Kabob": 0,
    "Stacked Enchiladas": 0,
}

MENU_ROT = ["Fresh Fish", "Chicken Breast", "Steak"]
MANDATORY_FOOD = []
RAINING_HOURS = 4

AVAILABLE_PURCHASES = {
    "Hash Browns": 750,
    "Breakfast Sandwich": 1000,
    "Pancakes": 900,
    "Fried Rice": 1200,
    "Lobster": 2500,
    "Banana Foster": 1400,
    "Shish Kabob": 1900,
    "Stacked Enchiladas": 1100,
    "Cold Beer": 600,
    "French Fries": 600,
    "Baked Potato": 1000,
    "Nachos": 600,
    "Lasagna": 600,
    "Fresh Fish": 2000,
    "Wine": 1800,
}

UPGRADE_BUDGET = 907
