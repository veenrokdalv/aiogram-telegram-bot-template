import logging
from urllib.parse import urlparse

import click
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.strategy import FSMStrategy
from aiogram.utils.i18n import I18n
from aiogram.webhook.aiohttp_server import TokenBasedRequestHandler, setup_application
from aiohttp.web import run_app
from aiohttp.web_app import Application
from aioredis import Redis

import loggers
from config import settings

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command(name='webhook')
@click.option('-wu', '--webhook-url', required=True)
@click.option('-sh', '--server-host', default='localhost')
@click.option('-sp', '--server-port', default=8000)
@click.option('-sk', '--secret-key', default=None)
@click.option('--drop-pending-updates/--no-drop-pending-updates', default=True)
def start_webhook(webhook_url: str, server_host: str, server_port: int, secret_key: str | None,
                  drop_pending_updates: bool):
    i18n, storage, dispatcher, bots, bot_settings, extra_data, web_app = _setup()
    extra_data.update({
        'webhook_url': webhook_url,
        'server_host': server_host,
        'server_port': server_port,
        'secret_key': secret_key,
        'drop_pending_updates': drop_pending_updates,
    })

    webhook_url_info = urlparse(webhook_url)
    web_handler = TokenBasedRequestHandler(dispatcher=dispatcher, bot_settings=bot_settings, **extra_data)
    web_handler.register(web_app, path=webhook_url_info.path)
    setup_application(web_app, dispatcher, bots=bots, **extra_data)
    run_app(app=web_app, host=server_host, port=server_port)


@cli.command(name='polling')
def start_polling():
    i18n, storage, dispatcher, bots, bot_settings, extra_data, web_app = _setup()
    dispatcher.run_polling(*bots, **extra_data)


def _setup() -> tuple[I18n, BaseStorage, Dispatcher, list[Bot], dict, dict, Application]:
    from bot import handlers, middlewares

    loggers.setup()

    logger.debug('Building bots')
    i18n = I18n(path=settings.LOCALES_DIR, default_locale=settings.DEFAULT_LANGUAGE_CODE, domain=settings.I18N_DOMAIN)
    bot_settings = {'parse_mode': settings.PARSE_MODE}
    bots = [Bot(token=_token, **bot_settings) for _token in settings.TELEGRAM_BOT_TOKENS]

    storage = RedisStorage(
        redis=Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True, )
    )

    dispatcher = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
    )

    middlewares.setup(dispatcher=dispatcher, i18n=i18n)
    handlers.setup(dispatcher=dispatcher)

    extra_data = {
        'i18n': i18n,
    }
    web_app = Application()

    return i18n, storage, dispatcher, bots, bot_settings, extra_data, web_app


if __name__ == '__main__':
    cli()
