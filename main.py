import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.strategy import FSMStrategy
from aiogram.utils.i18n import I18n
from aioredis import Redis

import loggers
from bot import handlers, middlewares
from config import settings

logger = logging.getLogger(__name__)


def main():
    """Point of entry"""

    logger.debug('Building bots')

    i18n = I18n(path=settings.LOCALES_DIR, default_locale=settings.DEFAULT_LANGUAGE_CODE, domain=settings.I18N_DOMAIN)

    bots = [Bot(token=_token, parse_mode=settings.PARSE_MODE) for _token in settings.TELEGRAM_BOT_TOKENS]

    storage = RedisStorage(
        redis=Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True,)
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

    dispatcher.run_polling(*bots, **extra_data)


loggers.setup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Stopped!')
else:
    logger.warning('Use: python main.py')
