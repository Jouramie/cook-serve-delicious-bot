from threading import Thread

import AppKit
import PIL.ImageGrab
import Quartz
import numpy as np

from kit._base_sensor_util import Region, GameCamera


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


def create_game_camera(game_name: str) -> GameCamera:
    return DarwinCamera(game_name)


class DarwinCamera(GameCamera):
    def __init__(self, game_name: str):
        super().__init__(game_name)
        self._thread = Thread(target=self._capture_loop)
        self._running = True

        self._last_frame = None
        self._last_frame_timestamp = None

    def calibrate(self):
        self.region = locate_window(self.game_name)

    def get_latest_frame(self) -> np.ndarray:
        return self._last_frame

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
            self._last_frame, self._last_frame_timestamp = self.capture_now()
