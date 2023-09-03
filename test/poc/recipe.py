import time

from pynput.keyboard import Controller, Key

keyboard = Controller()


if __name__ == "__main__":
    recipe = ["r", "c", "b", "o", "m", "g", Key.enter]

    for k in recipe:
        keyboard.tap(k)

    time.sleep(1)
