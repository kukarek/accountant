from aiogram import Bot
from controllers.handlers.user_handlers import dp, Settings
import database
import asyncio


async def start():

    bot = Bot(token = Settings().tokens.API_TOKEN_TEST)
    
    database.init()

    await dp.start_polling(bot)

loop = asyncio.get_event_loop()
results = loop.run_until_complete(start())
