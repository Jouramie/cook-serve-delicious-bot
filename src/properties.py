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
    "Fried Chicken": 1,
    "Soda Fountain": 2,
    "French Fries": 1,
    "Salad": 3,
    "Ice Cream": 3,
    "Baked Potato": 3,
    "Nachos": 1,
    "Lasagna": 1,
    "Fresh Fish": 3,
    "Chicken Breast": 4,
    "Pasta": 3,
    "Wine": 1,
    "Pizza": 3,
    "Burger": 3,
    "Steak": 3,
    "Soups": 3,
    "Coffee": 0,
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

MENU_ROT = ["Baked Potato"]
MANDATORY_FOOD = ["Baked Potato", "Fresh Fish", "Wine", "Steak"]
