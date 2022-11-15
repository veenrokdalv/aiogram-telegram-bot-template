from aiogram import Dispatcher, Router


router = Router()


# from bot.filters import ChatTypesFilter
# from bot.utils.throttling import rate_limit
#
# @rate_limit()
# @router.message(ChatTypesFilter('private'))
# async def handler_command_start(message: Message):
#     await message.answer(text=f'Hello, {message.from_user.full_name}')


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
