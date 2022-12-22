# -*- coding: utf-8 -*-

import pyaudio
from ..core.iaudio import IAudio


def play(audio: IAudio) -> None:
    """
    Plays the passed IAudio.
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(audio.get_sample_width()),
        channels=1,
        rate=audio.get_framerate(),
        output=True
    )
    to_bytes = audio.get_values().tobytes()
    chunk, i = 2048, 0
    while True:
        data = to_bytes[(i * chunk): ((i + 1) * chunk)]
        if len(data) == 0:
            break
        stream.write(data)
        i += 1
    stream.close()
    p.terminate()
