from aiogram import Dispatcher

import loggers
from bot.handlers import hooks, private, group, channel


def setup(*, dispatcher: Dispatcher):
    loggers.bot.debug('Setup handlers')

    private.setup(dispatcher=dispatcher)
    group.setup(dispatcher=dispatcher)
    channel.setup(dispatcher=dispatcher)

    dispatcher.startup.register(hooks.on_startup)
    dispatcher.shutdown.register(hooks.on_shutdown)
