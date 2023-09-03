from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

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


class GameCamera(ABC):
    def __init__(self, game_name: str):
        self.game_name = game_name
        self.region = None

        self._last_frame_timestamp = None
        self._last_frame = None

    @abstractmethod
    def calibrate(self):
        raise NotImplementedError

    @abstractmethod
    def get_latest_frame(self) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def start(self):
        self.calibrate()

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def capture_now(self) -> tuple[np.ndarray, datetime]:
        raise NotImplementedError
