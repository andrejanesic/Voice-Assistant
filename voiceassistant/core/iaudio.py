# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import numpy as np


class IAudio(ABC):
    """Wrapper for audio input data (sample values, framerate, etc.)"""

    @abstractmethod
    def get_values(self) -> np.ndarray:
        """Returns the values of the audio."""
        pass

    @abstractmethod
    def get_framerate(self) -> int:
        """Returns the audio framerate."""
        pass

    @abstractmethod
    def get_sample_width(self) -> int:
        """Returns the sample width."""
        pass

    @abstractmethod
    def set_values(self, values: np.ndarray) -> None:
        """Sets the values of the audio."""
        pass

    @abstractmethod
    def set_framerate(self, framerate: int) -> None:
        """Sets the audio framerate."""
        pass

    @abstractmethod
    def set_sample_width(self, sample_width: int) -> None:
        """Sets the sample width."""
        pass
