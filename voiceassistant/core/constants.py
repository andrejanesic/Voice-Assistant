# -*- coding: utf-8 -*-

import os


# Errors
ERR_NO_WORDS_FOUND = "No words found in audio"
ERR_FILE_NOT_EXIST = "File does not exist: %s"
ERR_ODD_WORD_INDICES_COUNT = "Detected odd number of word indices: %d"
ERR_NO_LOG_MESSAGE_SPECIFIED = "You didn't specify a message to log!"

# Parameters
PARAM_EXTRACT_P = 2000
PARAM_EXTRACT_R = 7500
PARAM_NLP_MAX_LEN = 256

# Logging
LOG_PREFIX_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_TYPES = ["ERROR", "WARNING", "INFO", "DEBUG"]

# Resources
RES_DIR = os.path.dirname(os.path.realpath(__file__)) + '/../../res'
RES_S2T_DIR = f"{RES_DIR}/wav2vec"
RES_S2T_MODEL = f"{RES_DIR}/wav2vec/model"
RES_NLP_MODEL = f"{RES_DIR}/nlp/model"
RES_NLP_TOKENIZER = f"{RES_DIR}/nlp/tokenizer"

# Output
AUDIO_OUT = "./audio_out.wav"
