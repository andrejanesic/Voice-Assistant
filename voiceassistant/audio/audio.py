# -*- coding: utf-8 -*-

from ..core.iaudio import IAudio
import numpy as np

class Audio(IAudio):

    def __init__(self, values: np.ndarray, framerate: int, sample_width: int) -> None:
        super().__init__()
        self.__values = values
        self.__framerate = framerate
        self.__sample_width = sample_width
    
    def get_values(self) -> np.ndarray:
        return self.__values

    def set_values(self, values: np.ndarray) -> None:
        self.__values = values

    def get_framerate(self) -> int:
        return self.__framerate

    def set_framerate(self, framerate: int) -> None:
        self.__framerate = framerate
    
    def get_sample_width(self) -> int:
        return self.__sample_width

    def set_sample_width(self, sample_width: int) -> None:
        self.__sample_width = sample_width
