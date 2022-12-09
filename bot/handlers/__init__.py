from aiogram import Dispatcher
from aiohttp.web_app import Application

import loggers
from bot.handlers import hooks, private, group, channel, web


def setup(*, dispatcher: Dispatcher, web_app: Application):
    loggers.bot.debug('Setup handlers')

    private.setup(dispatcher=dispatcher)
    group.setup(dispatcher=dispatcher)
    channel.setup(dispatcher=dispatcher)
    hooks.setup(dispatcher=dispatcher)

    web.setup(web_app=web_app)
