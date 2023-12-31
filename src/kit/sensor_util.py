from __future__ import annotations

import sys

import cv2
import numpy as np

from kit._base_sensor_util import Region, HsvColorBoundary

if sys.platform == "darwin":
    from kit.darwin_sensor_util import locate_window, create_camera
elif sys.platform == "win32":
    from kit.win32_sensor_util import locate_window, create_camera

assert locate_window
assert create_camera


def crop(img: np.ndarray, region: Region) -> np.ndarray:
    return img[
        region.top : region.bottom,
        region.left : region.right,
    ]


def mask(img: np.ndarray, color_boundary: HsvColorBoundary):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, color_boundary.lower_bound, color_boundary.upper_bound)
