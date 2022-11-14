from aiogram import Dispatcher


# async def handler_new_message(message: Message, bot: Bot):
#     await send_copy_messages(
#         bot=bot,
#         message=message,
#         chat_ids=[1, 2, 3, 4, 5]
#     )


def setup(*, dispatcher: Dispatcher):
    # dispatcher.message.register(handler_new_message, ChatTypesFilter('channel'))
    pass
