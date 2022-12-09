from aiogram import Bot
from aiogram.utils.i18n import I18n

from bot.utils.bot import set_my_commands


async def on_startup(bots: list[Bot], i18n: I18n, **kwargs):
    for bot in bots:
        await set_my_commands(bot=bot, i18n=i18n)
        if 'webhook_url' in kwargs:
            await bot.set_webhook(
                url=kwargs['webhook_url'].format(bot_token=bot.token),
                secret_token=kwargs['secret_key'],
                drop_pending_updates=kwargs['drop_pending_updates'],
            )


async def on_shutdown(bots: list[Bot], i18n: I18n, **kwargs):
    for bot in bots:
        await bot.delete_my_commands()
        if 'webhook_url' in kwargs:
            await bot.delete_webhook(
                drop_pending_updates=kwargs['drop_pending_updates'],
            )
