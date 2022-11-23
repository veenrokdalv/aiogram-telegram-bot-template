from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram import Dispatcher
from aiogram.types import Message
from cachetools import TTLCache

import loggers
from bot.utils.throttling import Throttling, parse_number_of_messages_by_throttle_name, parse_seconds_by_throttle_name
from config import settings


class MessageThrottlingMiddleware(BaseMiddleware):
    """
    Throttling messages
    """
    storage = {
        name: TTLCache(maxsize=10_000, ttl=parse_seconds_by_throttle_name(name)) for name in settings.THROTTLES.keys()
    }

    async def __call__(self, handler: Callable, event: Message, data: dict) -> Any:  # pragma: no cover
        callback_handler = data['handler'].callback

        handler_has_throttling_key = hasattr(callback_handler, settings.THROTTLING_KEY)

        if event.chat.type != 'private' or not handler_has_throttling_key:
            return await handler(event, data)

        name = getattr(callback_handler, settings.THROTTLING_KEY)

        key = self._make_key(event)

        if key not in self.storage[name]:
            self.storage[name][key] = 0

        self.storage[name][key] += 1

        try:
            await self._throttle_message(name, event)
        except Throttling:
            await self._process_message_throttling(name, event)
        else:
            return await handler(event, data)

    async def _throttle_message(self, name: str, message: Message):
        """Throttle message"""
        key = self._make_key(message)
        number_of_messages = parse_number_of_messages_by_throttle_name(name)

        if self.storage[name][key] > number_of_messages:
            raise Throttling()

    async def _process_message_throttling(self, name: str, message: Message):
        """Process message throttling"""
        key = self._make_key(message)
        number_of_messages = parse_number_of_messages_by_throttle_name(name)

        if message.chat.type == 'private':
            if self.storage[name][key] == number_of_messages + 1:
                await message.answer(f'Flood! You are temporarily muted, please wait!')

        elif message.chat.type in {'group', 'supergroup'}:
            await message.chat.ban_sender_chat(message.from_user.id)

    def _make_key(self, message: Message) -> str:
        key = '{chat_id}:{user_id}'.format(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
        return key


def setup(*, dispatcher: Dispatcher, **kwargs):
    loggers.bot.debug('Setup middlewares')
    dispatcher.message.middleware.register(MessageThrottlingMiddleware())
