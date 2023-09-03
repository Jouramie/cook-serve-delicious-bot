import PIL.ImageGrab

from kit import img_logger
from kit.profiling import timeit


@timeit(print_each_call=True)
def screenshot():
    return PIL.ImageGrab.grab()


if __name__ == "__main__":
    try:
        sc = screenshot()
        img_logger.log_now(sc)
    finally:
        img_logger.finalize()
