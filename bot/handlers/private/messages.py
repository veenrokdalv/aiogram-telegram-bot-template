from aiogram import Dispatcher


# async def handler_command_start(message: Message):
#     await message.answer(text=f'Hello, {message.from_user.full_name}',)


def setup(*, dispatcher: Dispatcher):
    # dispatcher.message.register(handler_command_start, ChatTypesFilter('private'))
    pass
