import datetime as dt
from typing import Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, TelegramObject, User
from cachetools import TTLCache

import loggers
from bot.utils.throttling import Throttling, parse_number_of_messages_by_throttle_name, parse_seconds_by_throttle_name
from config import settings


class MessageThrottlingInPrivateChatMiddleware(BaseMiddleware):
    """
    Throttling messages in private chat
    """
    storage = {
        name: TTLCache(maxsize=10_000, ttl=parse_seconds_by_throttle_name(name)) for name in settings.THROTTLES.keys()
    }

    async def __call__(self, handler: Callable, event: Message, data: dict) -> Any:  # pragma: no cover

        if not ('handler' in data and hasattr(data['handler'], 'callback')):
            return await handler(event, data)

        if event.chat.type != 'private' or not hasattr(data['handler'].callback, settings.THROTTLING_KEY):
            return await handler(event, data)

        name = getattr(data['handler'].callback, settings.THROTTLING_KEY)

        if data['event_from_user'].id not in self.storage[name]:
            self.storage[name][data['event_from_user'].id] = 0

        self.storage[name][data['event_from_user'].id] += 1

        try:
            await self._throttle_message(name, event)
        except Throttling:
            await self._process_message_throttling(name, event)
        else:
            return await handler(event, data)

    async def _throttle_message(self, name: str, message: Message):
        """Throttle message"""
        number_of_messages = parse_number_of_messages_by_throttle_name(name)

        if self.storage[name][message.from_user.id] > number_of_messages:
            raise Throttling()

    async def _process_message_throttling(self, name: str, message: Message):
        """Process message throttling"""
        number_of_messages = parse_number_of_messages_by_throttle_name(name)
        if self.storage[name][message.from_user.id] == number_of_messages + 1:
            await message.answer(f'Flood! You are temporarily muted, please wait!')


def setup(*, dispatcher: Dispatcher, **kwargs):
    loggers.bot.debug('Setup middlewares')
    dispatcher.message.middleware.register(MessageThrottlingInPrivateChatMiddleware())
