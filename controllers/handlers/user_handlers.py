from ..keyboards import *
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from ..keyboards.keyboards import *
from aiogram.dispatcher.filters import Text
from ..filters.main_filter import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from models import Transaction, Transactions_Categories, User
from datetime import datetime, timedelta


class States(StatesGroup):

    date = State()
    amount = State()
    category = State()

async def adding_entry(message: types.Message, state: FSMContext):
    
    current_state = await state.get_state()

    if not current_state:
        
        await state.update_data(type=message.text)
        await message.answer("Выберите день: ", reply_markup=keyboard("Сегодня", "Вчера", "Отмена"))
        await States.date.set()

    elif message.text == "Отмена":

        await state.reset_state(with_data=True)

        await message.answer("Запись удалена!", reply_markup=keyboard("Добавить запись", "Удалить запись", "Статистика")) 

    elif current_state == States.date.state:

        if message.text == "Сегодня": date = datetime.now().strftime(Settings().format.datetime)
        elif message.text == "Вчера": date = (datetime.now() - timedelta(days=1)).strftime(Settings().format.datetime)

        await state.update_data(date=date)
        await message.answer("Введите сумму: ", reply_markup=keyboard("Отмена"))
        await States.amount.set()

    elif current_state == States.amount.state:

        await state.update_data(amount=message.text)
        await message.answer("Введите категорию: ", reply_markup=keyboard(*[item.value for item in Transactions_Categories], "Отмена"))
        await States.category.set()

    elif current_state == States.category.state:

        await state.update_data(category=message.text)

        data = await state.get_data()

        transaction = Transaction(
            data['date'],
            data['amount'],
            data['category']
        )

        User(message.from_id, message.from_user.first_name).update(transaction)

        await state.reset_state(with_data=True)

        await message.answer("Запись добавлена!", reply_markup=keyboard("Добавить запись", "Удалить запись", "Статистика"))


async def start_status_handler(message: Message):
    
    User(message.from_id, message.from_user.first_name)

    text = ("Бим бим бам бам\n\n"+
            "Скока заработави?")

    await message.answer(text, reply_markup = keyboard("Добавить запись", "Удалить запись", "Статистика"))

async def remove_entry(message: Message):

    #нужно разбить на блоки по 10 транзакций, чтобы обойти ограничения по количеству кнопок в одном сообщении
    transactions = User(message.from_id, message.from_user.first_name).transactions

    if not transactions:
        await message.answer("Нет данных")
        return
    
    mess = await message.answer("Список записей:")
    await mess.edit_reply_markup(inline_keyboard(*[(f"{item.datetime[:5]} {item.amount}р {item.category}", f"Remove/{item.datetime}/{mess.message_id}/{message.from_id}") for item in transactions]))


async def removing_entry(query: CallbackQuery):

    data = query.data.split('/')

    await query.bot.delete_message(data[3], data[2])

    User(data[3], query.from_user.first_name).remove_transaction(data[1])

    await query.bot.send_message(data[3], "Запись удалена!", reply_markup = keyboard("Добавить запись", "Удалить запись", "Статистика"))

def register_user_handlers(dp: Dispatcher):

    dp.register_message_handler(start_status_handler, isUser(), commands=['start'])
    dp.register_message_handler(adding_entry, isUser(), Text(equals=("Добавить запись")))
    dp.register_message_handler(remove_entry, isUser(), Text(equals=("Удалить запись")))
    dp.register_message_handler(adding_entry, isUser(), state=States.amount)
    dp.register_message_handler(adding_entry, isUser(), state=States.category)
    dp.register_message_handler(adding_entry, isUser(), state=States.date)

    dp.register_callback_query_handler(removing_entry, lambda query: query.data.startswith("Remove"))










