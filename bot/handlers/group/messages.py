from aiogram import Dispatcher, Router

router = Router()

# from aiogram.types import Message
# from bot.filters import ChatTypesFilter
# from bot.utils.throttling import rate_limit

# @rate_limit()
# @router.message(ChatTypesFilter('group', 'supergroup'))
# async def handler_echo(message: Message):
#     await message.answer(text=message.text)


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
