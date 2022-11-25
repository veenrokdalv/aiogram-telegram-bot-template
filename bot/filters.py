from aiogram.filters import Filter
from aiogram.filters.text import TextType
from aiogram.types import Message, CallbackQuery, InlineQuery
from aiogram.utils.i18n import I18n
from cachetools.func import lru_cache

import loggers
from config import settings


class InternationalMessageTextFilter(Filter):
    __slots__ = ("text",)

    def __init__(self, *text: TextType):
        """
        :param text: Text equals value or one of values
        """
        self._text = set(text)

    def __str__(self) -> str:
        return self._signature_to_string(text=self.text, )

    @lru_cache
    def get_text(self, i18n: I18n):
        return {i18n.gettext(_text, locale=settings.DEFAULT_LANGUAGE_CODE) for _text in self._text}

    async def __call__(self, message: Message, i18n: I18n):
        message_text = message.text or message.caption or ""

        if not message_text:
            return False

        message_text = i18n.gettext(message_text, locale=settings.DEFAULT_LANGUAGE_CODE)

        text = self.get_text(i18n=i18n)

        return message_text in text


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
