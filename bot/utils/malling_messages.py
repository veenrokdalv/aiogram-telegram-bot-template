from asyncio import sleep
from uuid import uuid4

from aiogram import Bot
from aiogram.types import Message

import loggers


async def send_text_messages(bot: Bot, text: str, chat_ids: list[int], **extra_options) -> int:
    malling_uuid = str(uuid4())
    loggers.bot.info(f'Start malling text [botId:{bot.id}] [mallingUUID:{malling_uuid}]')

    success = 0

    for number, chat_id in enumerate(chat_ids, start=1):
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                **extra_options
            )
        except Exception as err:
            loggers.bot.warning(
                f'Fail sending text message in chat '
                f'[bot:{bot.id}] [chatId:{chat_id}] [mallingUUID:{malling_uuid}] [error:{err}]'
            )
            continue

        success += 1

        if number % 10 == 0:
            await sleep(0.5)

    count_chats = len(chat_ids)
    loggers.bot.info(
        f'Sent text messages {success}/{count_chats} [botId:{bot.id}] [mallingUUID:{malling_uuid}]'
    )
    return success


async def send_copy_messages(bot: Bot, message: Message, chat_ids: list[int], **extra_options) -> int:
    malling_uuid = str(uuid4())
    loggers.bot.info(f'Start malling copy message [botId:{bot.id}] [mallingUUID:{malling_uuid}]')

    success = 0

    for number, chat_id in enumerate(chat_ids, start=1):
        try:
            await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                **extra_options
            )
        except Exception as err:
            loggers.bot.warning(
                f'Fail sending copy message in chat '
                f'[bot:{bot.id}] [chatId:{chat_id}] [mallingUUID:{malling_uuid}] [error:{err}]'
            )
            continue

        success += 1

        if number % 10 == 0:
            await sleep(0.5)

    count_chats = len(chat_ids)
    loggers.bot.info(
        f'Sent copy messages {success}/{count_chats} [botId:{bot.id}] [mallingUUID:{malling_uuid}]'
    )
    return success


async def forward_messages(bot: Bot, message: Message, chat_ids: list[int], **extra_options) -> int:
    malling_uuid = str(uuid4())
    loggers.bot.info(f'Start forward messages [botId:{bot.id}] [mallingUUID:{malling_uuid}]')

    success = 0

    for number, chat_id in enumerate(chat_ids, start=1):
        try:
            await bot.forward_message(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                **extra_options
            )
        except Exception as err:
            loggers.bot.warning(
                f'Fail forwarding message in chat '
                f'[bot:{bot.id}] [chatId:{chat_id}] [mallingUUID:{malling_uuid}] [error:{err}]'
            )
            continue

        success += 1

        if number % 10 == 0:
            await sleep(0.5)

    count_chats = len(chat_ids)
    loggers.bot.info(
        f'Forwarded messages {success}/{count_chats} [botId:{bot.id}] [mallingUUID:{malling_uuid}]'
    )
    return success
