from aiogram import Dispatcher, Router

router = Router()


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
