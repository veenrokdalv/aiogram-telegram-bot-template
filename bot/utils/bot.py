from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import run_app
from aiohttp.web_app import Application

import loggers


def setup_webhook(*bots: Bot, dispatcher: Dispatcher, **extra_data):
    loggers.bot.debug('Setup webhooks')
    webhook_url_postfix = 'webhook/{bot.id}'
    web_app = Application()
    for bot in bots:
        web_handler = SimpleRequestHandler(dispatcher=dispatcher, bot=bot, **extra_data)
        web_handler.register(web_app, path='/' + webhook_url_postfix.format(bot=bot))

    setup_application(web_app, dispatcher, bots=bots, **extra_data)
    run_app(app=web_app, host='127.0.0.1', port=8080)


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
