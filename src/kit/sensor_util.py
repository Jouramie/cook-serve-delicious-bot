from collections import namedtuple
from dataclasses import dataclass

import cv2
import numpy as np

Region = namedtuple("Region", ["left", "top", "right", "bottom"])


@dataclass(frozen=True)
class HsvColorBoundary:
    lower_bound: np.ndarray
    upper_bound: np.ndarray
    color: str | None = None


def crop(img: np.ndarray, region: Region) -> np.ndarray:
    return img[
        region.top : region.bottom,
        region.left : region.right,
    ]


def mask(img: np.ndarray, color_boundary: HsvColorBoundary):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, color_boundary.lower_bound, color_boundary.upper_bound)
