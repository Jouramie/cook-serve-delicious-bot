import sys


if sys.platform == "darwin":
    import PIL.ImageGrab
    import Quartz
    import AppKit

from kit import img_logger
from kit.profiling import timeit
from kit.sensor_util import Region


EXPECTED_WINDOW_NAME = "Cook Serve Delicious"


def grab_screenshot(region: Region | None = None):
    raise NotImplementedError()


@timeit(name="grab_screenshot", print_each_call=True)
def __grab_screenshot_darwin(region: Region | None = None):
    if region is None:
        return PIL.ImageGrab.grab()
    return PIL.ImageGrab.grab(region.corners)


def locate_window(name: str) -> Region:
    raise NotImplementedError()


def __locate_window_darwin(name: str) -> Region:
    running_apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
    target_app = next(a for a in running_apps if a.localizedName() == name)
    target_app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)

    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID
    )
    for win in windows:
        if name in "%s %s" % (win[Quartz.kCGWindowOwnerName], win.get(Quartz.kCGWindowName, "")):
            w = win["kCGWindowBounds"]
            return Region.of_box(w["X"], w["Y"], w["Width"], w["Height"])


if sys.platform == "darwin":
    locate_window = __locate_window_darwin
    grab_screenshot = __grab_screenshot_darwin


if __name__ == "__main__":
    try:
        img_logger.log_now(grab_screenshot(locate_window(EXPECTED_WINDOW_NAME)), "test.png")
    finally:
        img_logger.finalize()
