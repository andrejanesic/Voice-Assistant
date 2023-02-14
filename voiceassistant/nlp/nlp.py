# -*- coding: utf-8 -*-

from ..core import constants
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np

_nlp_model, _nlp_tokenizer = None, None


def analyze(inp: str) -> str:
    """
    Evaluates the emotions of the given command
    and returns a string representing the
    emotion.
    """

    global _nlp_model, _nlp_tokenizer

    if not _nlp_model:
        _nlp_model = BertForSequenceClassification.from_pretrained(
            constants.RES_NLP_MODEL
        )
        _nlp_model.eval()

    if not _nlp_tokenizer:
        _nlp_tokenizer = BertTokenizer.from_pretrained(
            constants.RES_NLP_TOKENIZER
        )

    inp = _nlp_tokenizer.encode(
        inp.strip(),
        add_special_tokens=True,
        max_length=constants.PARAM_NLP_MAX_LEN,
        pad_to_max_length=True
    )

    torch_inputs = torch.tensor(inp)
    attention_mask = torch.tensor([float(i > 0) for i in inp])

    torch_inputs = torch_inputs.reshape(1, -1)
    attention_mask = attention_mask.reshape(1, -1)

    out = _nlp_model(
        torch_inputs,
        token_type_ids=None,
        attention_mask=attention_mask
    )

    nlp_decode_arr = ["anger", "fear", "joy", "love", "sadness", "surprise"]
    emotion = nlp_decode_arr[np.argmax(out[0].cpu().detach().numpy())]
    return emotion
