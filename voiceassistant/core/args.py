# -*- coding: utf-8 -*-

from . import state
import argparse

def init_args() -> None:
    """
    Initializes program arguments.
    """

    parser = argparse.ArgumentParser(
        prog='Voice Assistant',
        description='Simple voice assistant built in Python/Tensorflow'
    )

    # Verbose
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        dest='verbose'
    )

    parsed = parser.parse_args()
    if not parsed:
        # Error in parsing
        return
    state.args = parsed