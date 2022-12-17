import collections
from functools import lru_cache
from typing import Union, Dict, Any

from aiogram import Dispatcher
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery, InlineQuery
from aiogram.utils.i18n import I18n

import loggers


class _I18nTextFilter(Filter):

    @staticmethod
    @lru_cache()
    def get_i18n_catalog(i18n: I18n):
        locales = i18n.locales
        catalog = collections.defaultdict(dict)

        for language_code, translations in locales.items():
            _catalog = translations._catalog.copy()
            del _catalog['']
            catalog[language_code].update(_catalog)
        return catalog


class I18nMessageTextFilter(_I18nTextFilter):

    def __init__(
            self,
            *message_id,
            ignore_case: bool = False
    ):
        self.message_id = message_id
        self.ignore_case = ignore_case

    async def __call__(
            self,
            event: Message,
            i18n: I18n,
    ) -> Union[bool, Dict[str, Any]]:
        if isinstance(event, Message):
            text = event.text or event.caption or ""
            if not text and event.poll:
                text = event.poll.question
        else:
            return False

        if self.ignore_case:
            text = text.lower()

        catalog = self.get_i18n_catalog(i18n=i18n)

        for language_code, translations in catalog.items():
            if self.ignore_case:
                translations = {msgid: msgstr.lower() for msgid, msgstr in translations.items()}

            for msgid, msgstr in translations.items():
                if text == msgstr and msgid in self.message_id:
                    return True

        return False


class I18nInlineQueryTextFilter(_I18nTextFilter):

    def __init__(
            self,
            *message_id,
            ignore_case: bool = False
    ):
        self.message_id = message_id
        self.ignore_case = ignore_case

    async def __call__(
            self,
            event: InlineQuery,
            i18n: I18n,
    ) -> Union[bool, Dict[str, Any]]:
        if isinstance(event, InlineQuery):
            text = event.query
        else:
            return False

        if self.ignore_case:
            text = text.lower().strip()

        catalog = self.get_i18n_catalog(i18n=i18n)

        for language_code, translations in catalog.items():
            if self.ignore_case:
                translations = {msgid: msgstr.lower() for msgid, msgstr in translations.items()}

            for msgid, msgstr in translations.items():
                if text.startswith(msgstr) and msgid in self.message_id:
                    query_args = text.replace(msgstr, '')
                    return {'query_args': query_args}

        return False


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


def setup(*, dispatcher: Dispatcher, i18n: I18n):
    dispatcher.update.filter()
