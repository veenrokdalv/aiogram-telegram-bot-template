from aiogram import Dispatcher, Router
from aiogram.types import Message
from aiogram.utils.i18n import I18n

from bot.filters import ChatTypesFilter

router = Router()



# @router.message(ChatTypesFilter('private'))
# async def handler_all_message(message: Message, i18n: I18n):
#     await message.answer(
#         text=i18n.gettext(
#             'Hi, {user_fullname}'
#         ).format(
#             user_fullname=message.from_user.full_name
#         )
#     )


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
