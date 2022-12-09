from aiogram import Dispatcher

from bot.handlers.group import messages, service_messages, callback_query, inlne_query


def setup(*, dispatcher: Dispatcher):
    messages.setup(dispatcher=dispatcher)
    service_messages.setup(dispatcher=dispatcher)
    callback_query.setup(dispatcher=dispatcher)
    inlne_query.setup(dispatcher=dispatcher)
