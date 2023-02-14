# -*- coding: utf-8 -*-

from . import constants
from . import state
import time


def log(*args: str) -> None:
    """
    Logs a message to program output. If flag
    -v not present, does not log.
    """

    if not state.args or not state.args.verbose:
        return

    if len(args) == 0:
        return

    log_type = 'INFO'
    if args[0].upper() in constants.LOG_TYPES:
        if len(args == 1):
            log('ERROR', constants.ERR_NO_LOG_MESSAGE_SPECIFIED)
            return
        log_type = args[0].upper()
        args = args[1:]
    
    time_formatted = time.strftime(
        constants.LOG_PREFIX_TIME_FORMAT,
        time.localtime()
    )
    log_prefix = f'[{time_formatted}][{log_type}] '
    args = list(args)
    args[0] = log_prefix + args[0]
    print(*args)
