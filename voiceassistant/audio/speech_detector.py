# -*- coding: utf-8 -*-

from ..core.iaudio import IAudio
from .audio import Audio
from .. import constants
import numpy as np
from types import List


def endpointing(audio: IAudio, p: int = 0, r: int = 0) -> tuple:
    """
    Finds the endpoints of speech on the IAudio.
    Returns noise mask and borders.
    """

    if p == 0:
        p = constants.PARAM_EXTRACT_P
    if r == 0:
        r = constants.PARAM_EXTRACT_R

    # Get the number of frames for the first 100ms.
    initial_t = 100
    initial_t = round((audio.get_framerate()) * initial_t / 1000)
    initial_f = np.absolute(audio.values[:initial_t])

    # Noise limit.
    noise_l = np.average(initial_f) + 2 * initial_f.std()
    noise_mask = np.zeros(audio.values.shape)

    # Window width (ms) for noise detection.
    window_w = 10
    window_w = round(audio.get_framerate() * window_w / 100)

    i = 0
    while i < len(audio.values):
        window_avg = np.average(np.absolute(audio.values[i:(i+window_w)]))
        j = 1 if window_avg > noise_l else 0
        noise_mask[i:(i+window_w)] = j
        i += window_w

    length = 0
    start = -1
    curr = 0
    while curr < len(noise_mask):
        if noise_mask[curr] == 1:
            if length < p:
                noise_mask[start+1:start+1+length] = 1
            start = curr
            length = 0
        curr += 1
        length += 1

    length = 0
    start = -1
    curr = 0
    while curr < len(noise_mask):
        if noise_mask[curr] == 0:
            if length < r:
                noise_mask[start+1:start+1+length] = 0
            start = curr
            length = 0
        curr += 1
        length += 1

    # Find borders of noise.
    shift_l = noise_mask.tolist().copy()
    shift_l.pop(0)
    shift_l.append(0)
    shift_r = noise_mask.tolist().copy()
    shift_r.pop()
    shift_r.insert(0, 0)
    noise_borders = ((noise_mask - np.array(shift_l) >
                      0) | (noise_mask - np.array(shift_r) > 0)).astype(int)
    noise_borders = (np.array(np.nonzero(noise_borders)) /
                     audio.get_framerate())[0].tolist()

    return (noise_mask, noise_borders)


def extract_speech(audio: IAudio, p: int = 0, r: int = 0) -> List[IAudio]:
    """
    Extracts a list of words detected in the
    IAudio as IAudio instances.
    """

    noise_mask, noise_borders = endpointing(audio, p, r)

    # Check if we detected any speech borders
    speech_detected = noise_mask.sum() > 0
    if speech_detected == False:
        print(constants.ERR_NO_WORDS_FOUND)
        return []

    if len(noise_borders) % 2 == 1:
        print(constants.ERR_ODD_WORD_INDICES_COUNT %
              len(noise_borders))
        return []

    words_raw = []
    values_cleaned = np.multiply(audio.values, noise_mask)
    i = 0
    while i < len(noise_borders):
        ind_l = int(noise_borders[i] * audio.get_framerate())
        ind_r = int(noise_borders[i + 1] * audio.get_framerate() + 1)
        words_raw.append(values_cleaned[ind_l:ind_r])
        i += 2

    words = []
    for w in words_raw:
        words.append(
            Audio(values=w,
                  framerate=audio.get_framerate(),
                  sample_width=audio.get_sample_width()
                  )
        )

    print(f"Extracted {len(words)} words")
    return words
