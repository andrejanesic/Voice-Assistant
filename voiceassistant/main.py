# -*- coding: utf-8 -*-

from .core import args, constants, helpers, state
from .externalapi import callers
from .audio import recorder, player
from .audio import speech_detector
from .speech2text import speech2text
from .text2speech import text2speech
from .nlp import nlp
import os


def main() -> None:
    """
    Main program loop.
    """

    # init program args
    args.init_args()

    # init params
    callers.load_geos()
    callers.load_cryptos()

    # run loop
    while True:
        try:
            print(constants.PRINT_HELPER)

            # program will exit after 60 seconds of silence
            audio_path = constants.AUDIO_IN
            audio = recorder.record(
                dur=constants.PARAM_REC_SEC,
                file_path=audio_path
            )

            speech_detected = speech_detector.extract_speech(
                audio=audio,
                p=constants.PARAM_EXTRACT_P,
                r=constants.PARAM_EXTRACT_R
            )

            if not speech_detected:
                helpers.log(constants.PRINT_BYE)
                return

            if not os.path.exists(audio_path):
                helpers.log(constants.ERR_FILE_NOT_EXIST % audio_path)
                return

            transcription = speech2text.transcribe(audio_path)

            if 'weather' in transcription:
                loc = callers.callers.get_params(transcription, callers._geos)
                command = callers.weather_api(loc)

            elif 'worth' in transcription:
                ticker = callers.get_params(transcription, callers._cryptos.keys())
                command = callers.crypto_api(ticker)

            elif 'time' in transcription:
                command = callers.time_api()

            elif 'joke' in transcription:
                command = callers.joke_api()

            elif 'flights' in transcription:
                loc = callers.get_params(transcription, callers._geos)
                command = callers.flights_api(loc)

            elif 'mean' in transcription:
                command = nlp.analyze(transcription)

            else:
                command = constants.ERR_COMMAND_NOT_RECOGNIZED

            audio_out = text2speech.generate(command, constants.AUDIO_OUT)

            player.play(audio_out)

        except KeyboardInterrupt:
            pass