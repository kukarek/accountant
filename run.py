from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from controllers.handlers import register_user_handlers
from misc.settings import Settings
import database


async def __on_start_up(dp: Dispatcher) -> None:

    register_user_handlers(dp)
    database.init()
    

def start() -> None:

    storage = MemoryStorage()
    bot = Bot(token = Settings().tokens.API_TOKEN_TEST)
    dp = Dispatcher(bot, storage = storage)

    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)

if __name__ == "__main__":

    start()