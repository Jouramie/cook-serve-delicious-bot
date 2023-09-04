import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

logger = logging.getLogger(__name__)


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
    def __init__(self, region: Region | None = None):
        logger.info(f"Instantiating camera to capture region f{region}")
        self.region = region

    @abstractmethod
    def get_latest_frame(self) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def flush(self):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def capture_now(self) -> np.ndarray:
        raise NotImplementedError
