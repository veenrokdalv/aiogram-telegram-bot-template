from aiogram import Dispatcher


# async def handler_join_member(message: Message):
#     await message.delete()
#     response_message = await message.answer(
#         text=f'Welcome, {message.from_user.id}'
#     )
#     await asyncio.sleep(15)
#     await response_message.delete()
#
#
# async def handler_left_member(message: Message):
#     await message.delete()
#     response_message = await message.answer(
#         text=f'Goodbye, {message.from_user.id}'
#     )
#     await asyncio.sleep(15)
#     await response_message.delete()


def setup(*, dispatcher: Dispatcher):
    # dispatcher.message.register(handler_join_member, MessageContentTypesFilter(ContentType.NEW_CHAT_MEMBERS), ChatTypesFilter('group', 'supergroup'))
    # dispatcher.message.register(handler_left_member, MessageContentTypesFilter(ContentType.LEFT_CHAT_MEMBER), ChatTypesFilter('group', 'supergroup'))
    pass
