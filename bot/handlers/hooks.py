from aiogram import Bot
from aiogram.utils.i18n import I18n

from bot.utils.bot import set_my_commands
from config import settings


async def on_startup(bots: list[Bot], i18n: I18n):
    webhook_url_postfix = 'webhook/{bot.id}'
    for bot in bots:
        await set_my_commands(bot=bot, i18n=i18n)
        await bot.set_webhook(settings.WEBHOOK_BASE_URL + webhook_url_postfix.format(bot=bot))


async def on_shutdown(bots: list[Bot]):
    for bot in bots:
        await bot.delete_my_commands()
