from aiogram import Dispatcher, Router

router = Router()


# from aiogram.types import CallbackQuery
# from bot.utils.throttling import rate_limit
#
# @rate_limit()
# @router.callback_query()
# async def handler_counter(callback_query: CallbackQuery):
#     await callback_query.answer('Text')

def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
