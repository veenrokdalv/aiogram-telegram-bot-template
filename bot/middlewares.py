from typing import Any, Callable, cast

from aiogram import BaseMiddleware, Bot
from aiogram import Dispatcher
from aiogram.types import Message, Update, User
from aiogram.utils.i18n import I18nMiddleware, I18n
from babel import Locale, UnknownLocaleError
from cachetools import TTLCache

import loggers
from bot.utils.throttling import parse_number_of_messages_by_throttle_name, parse_seconds_by_throttle_name
from bot.exceptions import Throttling
from config import settings


class TranslationMiddleware(I18nMiddleware):

    def __init__(self, i18n: I18n):
        self.i18n = i18n

        super().__init__(i18n=self.i18n)

    async def get_locale(self, event: Update, data: dict[str, Any]) -> str:
        locale = None

        if 'event_from_user' in data:
            locale = self._get_locale_from_event_user(data['event_from_user'])

        if locale is None:
            locale = settings.DEFAULT_LANGUAGE_CODE

        return locale

    def _get_locale_from_event_user(self, user: User) -> str | None:
        try:
            locale = Locale.parse(user.language_code, sep="-")
        except UnknownLocaleError:
            return None

        if locale.language not in self.i18n.available_locales:
            return None

        return cast(str, locale.language)


class MessageThrottlingMiddleware(BaseMiddleware):
    """
    Throttling messages
    If the user exceeds the limit of sent messages, described in settings.THROTTLES,
    the bot will stop responding to his messages.
    The bot will start responding to the user's messages
    again as soon as it stops flooding messages and restores its limits

    In _throttle_message define logic throttle message
    In _process_message_throttling define the behavior of the bot to flood the user
    """
    storage = {
        name: TTLCache(maxsize=10_000, ttl=parse_seconds_by_throttle_name(name)) for name in settings.THROTTLES.keys()
    }

    async def __call__(self, handler: Callable, event: Message, data: dict) -> Any:  # pragma: no cover
        callback_handler = data['handler'].callback
        bot = data['bot']

        if not hasattr(callback_handler, settings.THROTTLING_KEY):
            return await handler(event, data)

        name = getattr(callback_handler, settings.THROTTLING_KEY)

        key = self._make_key(bot, event)

        if key not in self.storage[name]:
            self.storage[name][key] = 0

        self.storage[name][key] += 1

        try:
            await self._throttle_message(name, bot, event)
        except Throttling:
            await self._process_message_throttling(name, bot, event)
        else:
            return await handler(event, data)

    async def _throttle_message(self, name: str, bot: Bot, message: Message):
        """Throttle message"""
        key = self._make_key(bot, message)
        number_of_messages = parse_number_of_messages_by_throttle_name(name)

        if self.storage[name][key] > number_of_messages:
            loggers.bot.debug(
                f'Message throttled [nameThrottle:{name}] [numberOfMessages:{number_of_messages}] [key:{key}]'
            )
            raise Throttling()

    async def _process_message_throttling(self, name: str, bot: Bot, message: Message):
        """Process message throttling"""
        # key = self._make_key(bot, message)
        # number_of_messages = parse_number_of_messages_by_throttle_name(name)

        # You can separate behavior in private chats and group/supergroup chats.

        # if message.chat.type == 'private':
        #     if self.storage[name][key] == number_of_messages + 1:
        #         await message.answer(f'Flood! You are temporarily muted, please wait!')
        #
        # elif message.chat.type in {'group', 'supergroup'}:
        #     if self.storage[name][key] == number_of_messages + 1:
        #         await message.chat.ban_sender_chat(message.from_user.id)

    def _make_key(self, bot: Bot, message: Message) -> str:
        key = '{bot_id}:{chat_id}:{user_id}'.format(
            bot_id=bot.id,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
        return key


def setup(*, dispatcher: Dispatcher, **kwargs):
    loggers.bot.debug('Setup middlewares')
    dispatcher.message.middleware.register(MessageThrottlingMiddleware())
    dispatcher.update.middleware.register(TranslationMiddleware(i18n=kwargs['i18n']))
