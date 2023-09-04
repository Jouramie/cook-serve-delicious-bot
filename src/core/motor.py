import logging

from pynput.keyboard import Key, Controller, Listener, KeyCode

from core.brain import Instruction, Keyboard

logger = logging.getLogger(__name__)

keyboard_controller = Controller()


class UnknownKeyException(Exception):
    pass


def to_pynput(key: str | int) -> Key | KeyCode:
    key = str(key)
    if len(key) == 1:
        return KeyCode.from_char(key)

    try:
        return getattr(Key, key)
    except AttributeError:
        raise UnknownKeyException


class PynputKeyboard(Keyboard):
    def send(self, key: str):
        keyboard_controller.tap(to_pynput(key))

    def wait_for(self, key: str):
        pynput_key = to_pynput(key)

        def on_press(pressed_key):
            print(f"Pressed {pressed_key}")

        def on_release(released_key):
            print(f"Released {released_key}")
            if released_key == pynput_key:
                return False
            return None

        with Listener(on_press, on_release) as listener:
            listener.join()


keyboard = PynputKeyboard()


def execute_instruction(instruction: Instruction):
    instruction(keyboard)


def select_task(task):
    keyboard_controller.tap(str(task))


def wait_for_game_to_start():
    logger.info("Waiting for 'enter' to start.")
    print("Waiting for 'enter' to start.")
    keyboard.wait_for("enter")
    logger.info("Enter pressed, resuming.")
    print("Enter pressed, resuming.")
