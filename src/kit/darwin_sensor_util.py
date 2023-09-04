import logging
import threading
import time
from threading import Thread

import AppKit
import PIL.ImageGrab
import Quartz
import numpy as np

from kit._base_sensor_util import Region, GameCamera

logger = logging.getLogger(__name__)


WINDOW_MARGIN_LEFT = 1
WINDOW_MARGIN_TOP = 29
WINDOW_MARGIN_RIGHT = 1
WINDOW_MARGIN_BOTTOM = 1


def locate_window(app_name: str) -> Region:
    running_apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
    target_app = next(a for a in running_apps if a.localizedName() == app_name)
    target_app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)

    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID
    )
    for win in windows:
        if app_name in "%s %s" % (win[Quartz.kCGWindowOwnerName], win.get(Quartz.kCGWindowName, "")):
            w = win["kCGWindowBounds"]
            return Region.of_box(w["X"], w["Y"], w["Width"], w["Height"])


def cut_window_margin(region: Region) -> Region:
    left, top, right, bottom = region.corners
    return Region.of_corners(
        left + WINDOW_MARGIN_LEFT, top + WINDOW_MARGIN_TOP, right - WINDOW_MARGIN_RIGHT, bottom - WINDOW_MARGIN_BOTTOM
    )


def create_camera(game: str | Region | None = None) -> GameCamera:
    if isinstance(game, str):
        game = cut_window_margin(locate_window(game))
    return DarwinCamera(game)


class DarwinCamera(GameCamera):
    def __init__(self, region: Region | None):
        super().__init__(region)
        self._thread = Thread(target=self._capture_loop)
        self._running = True

        self._last_frame = None
        self._last_frame_timestamp = None
        self._last_frame_lock = threading.Lock()

    def get_latest_frame(self) -> np.ndarray:
        while self._last_frame is None:
            time.sleep(0.01)

        with self._last_frame_lock:
            frame, self._last_frame = self._last_frame, None
            return frame

    def capture_now(self) -> np.ndarray:
        if self.region is None:
            return np.asarray(PIL.ImageGrab.grab())
        return np.asarray(PIL.ImageGrab.grab(self.region.corners))

    def start(self):
        self._thread.start()

    def stop(self):
        self._running = False

    def _capture_loop(self):
        while self._running:
            frame = self.capture_now()
            with self._last_frame_lock:
                self._last_frame = frame
