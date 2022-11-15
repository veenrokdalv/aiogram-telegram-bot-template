from aiogram import Dispatcher

import loggers
from bot.handlers.private import messages, callback_query, inlne_query


def setup(*, dispatcher: Dispatcher):
    messages.setup(dispatcher=dispatcher)
    callback_query.setup(dispatcher=dispatcher)
    inlne_query.setup(dispatcher=dispatcher)
