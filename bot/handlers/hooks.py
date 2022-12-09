from aiogram import Bot
from aiogram.utils.i18n import I18n

from bot.utils.bot import set_my_commands
from config import settings


async def on_startup(bots: list[Bot], i18n: I18n):
    for bot in bots:
        await set_my_commands(bot=bot, i18n=i18n)
        await bot.set_webhook(
            url=settings.WEBHOOK_URL.format(bot_token=bot.token),
            secret_token=settings.SECRET_KEY,
            drop_pending_updates=True,
        )


async def on_shutdown(bots: list[Bot]):
    for bot in bots:
        await bot.delete_my_commands()
        await bot.delete_webhook(
            drop_pending_updates=True,
        )
