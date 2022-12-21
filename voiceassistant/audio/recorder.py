# -*- coding: utf-8 -*-

# Code based on the following StackOverflow answer:
# https://stackoverflow.com/a/6743593

from ..core.iaudio import IAudio
from .audio import Audio
from sys import byteorder
from array import array
import pyaudio
import time


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
    dur: float = -1.0
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
        pass

    sample_width = p.get_sample_size(format)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    return Audio(values=r,
                 framerate=framerate,
                 sample_width=sample_width)
