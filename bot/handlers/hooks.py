from aiogram import Bot

from bot.utils.bot import set_my_commands


async def on_startup(bots: list[Bot]):
    for bot in bots:
        await set_my_commands(bot)


async def on_shutdown(bots: list[Bot]):
    pass
