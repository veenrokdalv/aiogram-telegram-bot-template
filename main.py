import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from bot import handlers, middlewares
from config import settings
import loggers

logger = logging.getLogger(__name__)


async def main():
    """Point of entry"""

    logger.debug('Building bots')

    bots = [Bot(token=_token, parse_mode=settings.PARSE_MODE) for _token in settings.TELEGRAM_BOT_TOKENS]

    dispatcher = Dispatcher(
        storage=MemoryStorage(),
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
    )

    middlewares.setup(dispatcher=dispatcher)
    handlers.setup(dispatcher=dispatcher)

    extra_data = {

    }

    await dispatcher.start_polling(*bots, **extra_data)


if __name__ == '__main__':
    loggers.setup()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning('Stopped!')

else:
    logger.warning('Use: python main.py')
