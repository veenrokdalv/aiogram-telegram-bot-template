from aiogram import Dispatcher, Router

router = Router()


# from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
# from bot.filters import ChatTypesFilter

# @router.inline_query(ChatTypesFilter('sender'))
# async def handler_query_empty_from_sender(inline_query: InlineQuery):
#     results = [
#         InlineQueryResultArticle(
#             id='1',
#             title='Title',
#             input_message_content=InputTextMessageContent(
#                 message_text=(
#                     'Message text'
#                 )
#             )
#         )
#     ]
#
#     await inline_query.answer(results=results, )
#
#
# @router.inline_query(ChatTypesFilter('private'))
# async def handler_query_empty_from_private(inline_query: InlineQuery):
#     results = [
#         InlineQueryResultArticle(
#             id='1',
#             title='Title',
#             input_message_content=InputTextMessageContent(
#                 message_text=(
#                     'Message text'
#                 )
#             )
#         )
#     ]

#     await inline_query.answer(results=results, )


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
    pass
