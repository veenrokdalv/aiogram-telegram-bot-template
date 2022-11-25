from aiogram import Bot

from aiogram.utils.i18n import I18n

import loggers


async def set_my_commands(bot: Bot, i18n: I18n):
    loggers.bot.debug('Set bot commands')

    for locale in i18n.available_locales:
        pass

        # from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
        #
        # await bot.set_my_commands(
        #     commands=[
        #         BotCommand(
        #             command='start',
        #             description=i18n.gettext('Start bot', locale=locale)
        #         )
        #     ],
        #     language_code=locale,
        #     scope=BotCommandScopeAllPrivateChats
        # )

