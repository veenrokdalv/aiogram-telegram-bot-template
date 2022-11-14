from aiogram import Dispatcher


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
#
#     await inline_query.answer(results=results, )


def setup(*, dispatcher: Dispatcher):
    # dispatcher.inline_query.register(handler_query_empty_from_sender, ChatTypesFilter('sender'))
    # dispatcher.inline_query.register(handler_query_empty_from_private, ChatTypesFilter('private'))
    pass
