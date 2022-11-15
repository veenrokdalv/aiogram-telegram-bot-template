import datetime as dt
from typing import Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, TelegramObject, User
from cachetools import TTLCache

import loggers
from bot.utils.throttling import Throttling, parse_number_of_messages_by_throttle_name, parse_seconds_by_throttle_name
from config import settings


class PrivateThrottlingMiddleware(BaseMiddleware):
    """
    Throttling messages and callbacks in private chats
    """
    storage = {
        name: TTLCache(maxsize=10_000, ttl=parse_seconds_by_throttle_name(name)) for name in settings.THROTTLES.keys()
    }

    async def __call__(self, handler: Callable, event: Message | CallbackQuery, data: dict) -> Any:  # pragma: no cover

        if not ('handler' in data and hasattr(data['handler'], 'callback')):
            return await handler(event, data)

        if isinstance(event, Message):
            if event.chat.type != 'private':
                return await handler(event, data)
        elif isinstance(event, CallbackQuery):
            if event.message.chat.type != 'private':
                return await handler(event, data)
        else:
            return await handler(event, data)

        callback_handler = data['handler'].callback

        if not hasattr(callback_handler, settings.THROTTLING_KEY):
            return await handler(event, data)

        user_from_event: User = data['event_from_user']

        name: str = getattr(callback_handler, settings.THROTTLING_KEY)

        if user_from_event.id not in self.storage[name]:
            self.storage[name][user_from_event.id] = 0

        self.storage[name][user_from_event.id] += 1

        try:
            if isinstance(event, Message):
                await self._throttle_message(name, event)

            elif isinstance(event, CallbackQuery):
                await self._throttle_callback_query(name, event)

        except Throttling:
            if isinstance(event, Message):
                await self._process_message_throttling(name, event)

            elif isinstance(event, CallbackQuery):
                await self._process_callback_query_throttling(name, event)

            return
        else:
            return await handler(event, data)

    async def _throttle_message(self, name: str, message: Message):
        """Throttle message"""
        number_of_messages = parse_number_of_messages_by_throttle_name(name)

        if self.storage[name][message.from_user.id] > number_of_messages:
            raise Throttling()

    async def _throttle_callback_query(self, name: str, callback_query: CallbackQuery):
        """Throttle callback query"""
        number_of_messages = parse_number_of_messages_by_throttle_name(name)

        if self.storage[name][callback_query.from_user.id] > number_of_messages:
            raise Throttling()

    async def _process_message_throttling(self, name: str, message: Message):
        """Process message throttling"""
        seconds = parse_seconds_by_throttle_name(name)
        number_of_messages = parse_number_of_messages_by_throttle_name(name)
        if self.storage[name][message.from_user.id] == number_of_messages + 1:
            await message.answer(f'Flood! You are temporarily muted, please wait!')

    async def _process_callback_query_throttling(self, name: str, callback_query: CallbackQuery):
        """Process callback query throttling"""
        seconds = parse_seconds_by_throttle_name(name)
        number_of_messages = parse_number_of_messages_by_throttle_name(name)

        if self.storage[name][callback_query.from_user.id] == number_of_messages + 1:
            mute_up_to_datetime = dt.datetime.now(tz=settings.DEFAULT_TIME_ZONE) + dt.timedelta(seconds=seconds)
            mute_up_to_datetime_str = mute_up_to_datetime.strftime(settings.SHORT_DATETIME_FORMAT)
            await callback_query.answer(
                text=f'Mute up to {mute_up_to_datetime_str}',
                show_alert=True,
                cache_time=int(seconds)
            )


def setup(*, dispatcher: Dispatcher, **kwargs):
    loggers.bot.debug('Setup middlewares')
    dispatcher.message.middleware.register(PrivateThrottlingMiddleware())
    dispatcher.callback_query.middleware.register(PrivateThrottlingMiddleware())
