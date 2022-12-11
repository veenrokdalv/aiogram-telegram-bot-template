from aiogram import Bot, Router, Dispatcher
from aiogram.utils.i18n import I18n

from bot.utils.bot import set_my_commands
from config import settings

router = Router()


@router.startup()
async def on_startup(bots: list[Bot], i18n: I18n, **kwargs):
    for bot in bots:
        await set_my_commands(bot=bot, i18n=i18n)
        await bot.set_webhook(
            url=settings.WEBHOOK_URL.format(bot_token=bot.token),
            secret_token=settings.SECRET_KEY,
            drop_pending_updates=True,
        )


@router.shutdown()
async def on_shutdown(bots: list[Bot], i18n: I18n, **kwargs):
    for bot in bots:
        await bot.delete_my_commands()
        await bot.delete_webhook(
            drop_pending_updates=True,
        )


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
