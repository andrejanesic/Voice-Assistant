# -*- coding: utf-8 -*-

# Reference:
# https://www.kdnuggets.com/2021/03/speech-text-wav2vec.html

import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torch
from ..core import constants


# Load model
_s2t_model, _s2t_tokenizer = None, None


def transcribe(file_path: str) -> str:
    """
    Detects speech using trained Wav2Vec.
    """

    global _s2t_model, _s2t_tokenizer

    if not _s2t_model:
        _s2t_model = Wav2Vec2ForCTC.from_pretrained(
            f"{constants.RES_S2T_MODEL}")
    if not _s2t_tokenizer:
        _s2t_tokenizer = Wav2Vec2Tokenizer.from_pretrained(
            constants.RES_S2T_DIR)

    audio, _ = librosa.load(file_path, sr=16000)
    input_values = _s2t_tokenizer(audio, return_tensors="pt").input_values
    logits = _s2t_model(input_values).logits
    prediction = torch.argmax(logits, dim=-1)

    return _s2t_tokenizer.batch_decode(prediction)[0]
