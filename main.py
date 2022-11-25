import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.utils.i18n import I18n

from bot import handlers, middlewares
from config import settings
import loggers

logger = logging.getLogger(__name__)


async def main():
    """Point of entry"""

    logger.debug('Building bots')

    i18n = I18n(path=settings.LOCALES_DIR, default_locale=settings.DEFAULT_LANGUAGE_CODE, domain=settings.I18N_DOMAIN)

    bots = [Bot(token=_token, parse_mode=settings.PARSE_MODE) for _token in settings.TELEGRAM_BOT_TOKENS]

    dispatcher = Dispatcher(
        storage=MemoryStorage(),
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
    )

    middlewares.setup(dispatcher=dispatcher, i18n=i18n)
    handlers.setup(dispatcher=dispatcher)

    extra_data = {
        'i18n': i18n,
    }

    await dispatcher.start_polling(*bots, **extra_data)


loggers.setup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning('Stopped!')
else:
    logger.warning('Use: python main.py')
