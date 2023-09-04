from pynput.keyboard import Key, Controller, Listener, KeyCode

from core.brain import Instruction, Keyboard

key_mappings = {"enter": Key.enter, "esc": Key.esc}
keyboard_controller = Controller()


class UnknownKeyException(Exception):
    pass


def to_pynput(key: str) -> Key | KeyCode:
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
            if released_key == key:
                return False
            return None

        with Listener(on_press, on_release) as listener:
            listener.join()


keyboard = PynputKeyboard()


def execute_instruction(instruction: Instruction):
    instruction(keyboard)


def select_task(task):
    keyboard_controller.tap(str(task))
