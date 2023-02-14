# -*- coding: utf-8 -*-

# Code based on the following StackOverflow answers:
# https://stackoverflow.com/a/6743593
# https://stackoverflow.com/questions/40782159/writing-wav-file-using-python-numpy-array-and-wave-module

from ..core.iaudio import IAudio
from ..core import helpers, constants
from .audio import Audio
from sys import byteorder
from array import array
import numpy as np
import pyaudio
import time
import wave


def normalize(snd_data: array, maximum: int = 16384) -> array:
    """Average the volume out"""

    times = float(maximum)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r


def record(
    format: any = pyaudio.paInt16,
    framerate: int = 44100,
    chunk_size: int = 1024,
    dur: float = -1.0,
    file_path: str = None
) -> IAudio:
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio.
    """

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=1, rate=framerate,
                    input=True, output=True,
                    frames_per_buffer=chunk_size)

    r = array('h')

    try:
        t_start = time.time()
        while True:
            # little endian, signed short
            snd_data = array('h', stream.read(chunk_size))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            if dur == -1:
                # Await on break
                continue
            else:
                if time.time() - t_start > dur:
                    break

    except KeyboardInterrupt:
        helpers.log(constants.PRINT_RECORDING_DONE)
        pass

    sample_width = p.get_sample_size(format)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    
    if file_path:
        with wave.open(file_path, "w") as f:
            f.setnchannels(1)
            f.setsampwidth(sample_width)
            f.setframerate(framerate)
            f.writeframes(r.tobytes())

    return Audio(values=np.asarray(r),
                 framerate=framerate,
                 sample_width=sample_width)
