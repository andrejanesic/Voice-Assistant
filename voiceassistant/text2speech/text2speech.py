# -*- coding: utf-8 -*-
import tensorflow as tf

import numpy as np
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor
import soundfile as sf

from ..core.iaudio import IAudio
from ..audio.loader import load_wave

def generate(text: str, file_path: str) -> IAudio:
    """
    Generates speech from passed text parameter using
    FastSpeech2 (pretrained on LJSpeech.)
    """
    # initialize fastspeech2 model.
    fastspeech2 = TFAutoModel.from_pretrained(
        "tensorspeech/tts-fastspeech2-ljspeech-en")


    # initialize mb_melgan model
    mb_melgan = TFAutoModel.from_pretrained(
        "tensorspeech/tts-mb_melgan-ljspeech-en")


    # inference
    processor = AutoProcessor.from_pretrained(
        "tensorspeech/tts-fastspeech2-ljspeech-en")

    input_ids = processor.text_to_sequence(text)
    # fastspeech inference

    mel_before, mel_after, duration_outputs, _, _ = fastspeech2.inference(
        input_ids=tf.expand_dims(
            tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
        speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
        speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
    )

    # melgan inference
    audio_before = mb_melgan.inference(mel_before)[0, :, 0]
    # audio_after = mb_melgan.inference(mel_after)[0, :, 0]

    # save to file
    sf.write(file_path, audio_before, 22050, "PCM_16")
    # sf.write('./audio_after.wav', audio_after, 22050, "PCM_16")
    return load_wave(filename=file_path)
