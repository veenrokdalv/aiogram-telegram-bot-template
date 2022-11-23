from pytimeparse.timeparse import timeparse

import loggers
from config import settings


def rate_limit(*, name: str = 'default'):
    _validate_rate_limit(name)

    def wrapper(func):
        setattr(func, settings.THROTTLING_KEY, name)
        return func

    return wrapper


def _validate_name(name):
    if name not in settings.THROTTLES:
        raise ValueError(f'Key {name} undefined in config.settings.THROTTLE')


def _validate_rate_limit(name):
    _validate_name(name)
    try:
        parse_seconds_by_throttle_name(name)
        parse_number_of_messages_by_throttle_name(name)
    except (ValueError, TypeError) as error:
        loggers.bot.critical(f'Rate invalid format!')
        raise error


def parse_seconds_by_throttle_name(name: str) -> float:
    rate_limit = settings.THROTTLES[name]
    _, duration_raw = rate_limit.split('/')
    seconds = float(timeparse(duration_raw))
    return seconds


def parse_number_of_messages_by_throttle_name(name: str) -> int:
    rate_limit = settings.THROTTLES[name]
    number_of_messages, _ = rate_limit.split('/')
    number_of_messages = int(number_of_messages)
    return number_of_messages
