from aiogram import Dispatcher, Router

router = Router()


# from aiogram.types import Message
# from aiogram.utils.i18n import I18n
#
# from bot.filters import ChatTypesFilter, InternationalMessageTextFilter
# from bot.utils.throttling import rate_limit
#
#
# @rate_limit()
# @router.message(InternationalMessageTextFilter(button_menu), ChatTypesFilter('private'))
# async def handler_echo(message: Message, i18n: I18n):
#     await message.answer(
#         text=i18n.gettext(
#             'Hi, {user_fullname}'
#         ).format(
#             user_fullname=message.from_user.full_name
#         )
#     )


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
