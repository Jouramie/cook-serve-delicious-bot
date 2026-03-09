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
CURRENT_RESTAURANT_STARS = 3
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
    "Nachos": 2,
    "Lasagna": 4,
    "Fresh Fish": 4,
    "Chicken Breast": 4,
    "Pasta": 4,
    "Wine": 1,
    "Pizza": 4,
    "Burger": 3,
    "Steak": 4,
    "Soups": 4,
    "Coffee": 2,
    "Hash Browns": 0,
    "Breakfast Sandwich": 3,
    "Pancakes": 0,
    "Sushi": 2,
    "Fried Rice": 0,
    "Lobster": 2,
    "Banana Foster": 0,
    "Shish Kabob": 2,
    "Stacked Enchiladas": 2,
}

MENU_ROT = ["Steak", "Fresh Fish"]
MANDATORY_FOOD = ["Pizza", "Sushi", "Breakfast Sandwich", "Shish Kabob"]

# Use 0 if no rain, 4 if rain is announced (it seems to be from 10 am to 3 pm, not counting rush hour)
RAINING_HOURS = 4

AVAILABLE_PURCHASES = {
    # Speciality unlock
    "Hash Browns": 750,
    "Pancakes": 900,
    "Fried Rice": 1200,
    "Banana Foster": 1400,
    # Standard upgrade
    "Cold Beer": 600,
    "French Fries": 600,
    "Baked Potato": 1000,
    "Nachos": 900,
    "Wine": 1800,
    "Burger": 1500,
    # Speciality upgrade
    "Sushi": 1100,
    "Lobster": 2500,
    "Shish Kabob": 2500,
    "Stacked Enchiladas": 700,
}

UPGRADE_BUDGET = 1231
