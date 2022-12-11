import logging
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.strategy import FSMStrategy
from aiogram.utils.i18n import I18n
from aiogram.webhook.aiohttp_server import TokenBasedRequestHandler, setup_application
from aiohttp.web import run_app
from aiohttp.web_app import Application
from aioredis import Redis

import loggers
from bot import handlers, middlewares
from config import settings

logger = logging.getLogger(__name__)


def main():
    """Point of entry"""

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

    web_app = Application()
    middlewares.setup(dispatcher=dispatcher, i18n=i18n)
    handlers.setup(dispatcher=dispatcher, web_app=web_app)

    extra_data = {
        'i18n': i18n,
    }

    webhook_url_info = urlparse(settings.WEBHOOK_URL)
    web_handler = TokenBasedRequestHandler(dispatcher=dispatcher, bot_settings=bot_settings, **extra_data)
    web_handler.register(web_app, path=webhook_url_info.path)
    setup_application(web_app, dispatcher, bots=bots, **extra_data)
    run_app(app=web_app, host=settings.WEB_APP_HOST, port=settings.WEB_APP_PORT)


loggers.setup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Stopped!')
    except Exception as exc:
        logger.error(f'{exc}')
        raise exc
    finally:
        logger.info(f'Bot stopped')


else:
    logger.warning('Use: python main.py')
