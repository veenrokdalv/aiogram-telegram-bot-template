from aiogram import Dispatcher

import loggers


def setup(*, dispatcher: Dispatcher, **kwargs):
    loggers.bot.debug('Setup middlewares')
