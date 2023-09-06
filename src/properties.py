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
SCREENSHOT_LOGGER_ROLLING_IMAGE_AMOUNT = 50
SCREENSHOT_LOGGER_EDIT_ENABLED = True

# Loop
MOVEMENT_ENABLED = True
