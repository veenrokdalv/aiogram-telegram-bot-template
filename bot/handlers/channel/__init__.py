from aiogram import Dispatcher

from bot.handlers.channel import messages


def setup(*, dispatcher: Dispatcher):
    messages.setup(dispatcher=dispatcher)
