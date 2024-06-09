from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from controllers.handlers import register_user_handlers
from misc.settings import Settings
import database
import asyncio


async def start():

    storage = MemoryStorage()
    bot = Bot(token = Settings().tokens.API_TOKEN_TEST)
    dp = Dispatcher(storage = storage)
    register_user_handlers(dp)
    database.init()
    await dp.run_polling(bot)

if __name__ == "__main__":

    asyncio.run(start())
 