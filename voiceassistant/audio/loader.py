# -*- coding: utf-8 -*-

import wave
import numpy as np
from .. import constants
from .audio import Audio
from ..core.iaudio import IAudio
from typing import Optional


def load_wave(filename: str) -> Optional[IAudio]:
    """
    Reads the wave file from <filename>.
    Returns the file as an Audio object.
    """

    # This would normally go into a try-except clause but IO errors are not important for this program.
    try:
        wav = wave.open(filename, "r")
    except FileNotFoundError:
        print(constants.ERR_FILE_NOT_EXIST % filename)
        return None

    vals = np.frombuffer(wav.readframes(-1), np.int16)

    # Average of two channels if stereo file.
    if wav.getnchannels() > 1:
        ch1 = vals[0::2]
        ch2 = vals[1::2]

        # TODO this might be an SPOF, because we're averaging the two channels with floor division.
        vals = (ch1 + ch2) // 2

    return Audio(
        values=vals,
        framerate=wav.getframerate(),
        sample_width=wav.getsampwidth()
    )
