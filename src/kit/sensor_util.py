from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class HsvColorBoundary:
    lower_bound: np.ndarray
    upper_bound: np.ndarray
    color: str | None = None


@dataclass(frozen=True)
class Region:
    corner: np.ndarray
    size: np.ndarray

    @staticmethod
    def of_ndarrays(corner: np.ndarray, size: np.ndarray):
        return Region(corner.astype(np.int64), size.astype(np.int64))

    @staticmethod
    def of_corners(left, top, right, bottom):
        return Region.of_ndarrays(np.array([left, top]), np.array([right - left, bottom - top]))

    @staticmethod
    def of_box(left, top, width, height):
        return Region.of_ndarrays(np.array([left, top]), np.array([width, height]))

    @property
    def left(self) -> int:
        return self.corner[0]

    @property
    def top(self) -> int:
        return self.corner[1]

    @property
    def right(self) -> int:
        return self.corner[0] + self.size[0]

    @property
    def bottom(self) -> int:
        return self.corner[1] + self.size[1]

    @property
    def corners(self) -> tuple[int, int, int, int]:
        return self.left, self.top, self.right, self.bottom


def crop(img: np.ndarray, region: Region) -> np.ndarray:
    return img[
        region.top : region.bottom,
        region.left : region.right,
    ]


def mask(img: np.ndarray, color_boundary: HsvColorBoundary):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, color_boundary.lower_bound, color_boundary.upper_bound)
