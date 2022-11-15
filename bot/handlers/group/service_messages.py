from aiogram import Dispatcher, Router

router = Router()


# @router.message(MessageContentTypesFilter(ContentType.NEW_CHAT_MEMBERS), ChatTypesFilter('group', 'supergroup'))
# async def handler_join_member(message: Message):
#     await message.delete()
#     response_message = await message.answer(
#         text=f'Welcome, {message.from_user.id}'
#     )
#     await asyncio.sleep(15)
#     await response_message.delete()
#
# @router.message(MessageContentTypesFilter(ContentType.LEFT_CHAT_MEMBER), ChatTypesFilter('group', 'supergroup'))
# async def handler_left_member(message: Message):
#     await message.delete()
#     response_message = await message.answer(
#         text=f'Goodbye, {message.from_user.id}'
#     )
#     await asyncio.sleep(15)
#     await response_message.delete()


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
