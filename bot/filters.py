from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery, InlineQuery

import loggers


class ChatTypesFilter(Filter):

    def __init__(self, *chat_types: str):
        self._allow_chat_types = set(chat_types)

    async def __call__(self, event: Message | CallbackQuery | InlineQuery, *args, **kwargs):
        if isinstance(event, Message):
            return event.chat.type in self._allow_chat_types
        elif isinstance(event, CallbackQuery):
            return event.message.chat.type in self._allow_chat_types
        elif isinstance(event, InlineQuery):
            return event.chat_type in self._allow_chat_types
        else:
            loggers.bot.warning(f'Unexpected event type! [eventType:{type(event)}]')
            return False


class MessageContentTypesFilter(Filter):

    def __init__(self, *content_types: str):
        self._allow_content_types = set(content_types)

    async def __call__(self, event: Message, *args, **kwargs):
        if isinstance(event, Message):
            return event.content_type in self._allow_content_types
        else:
            loggers.bot.warning(f'Unexpected event type! [eventType:{type(event)}]')
            return False
