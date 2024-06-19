from ..keyboards import *
from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from ..keyboards.keyboards import *
from ..filters.main_filter import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from models import Transaction, Transactions_Categories, User
from stats import Stats
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime, timedelta
from misc.settings import Settings

dp = Dispatcher(storage = MemoryStorage())

class States(StatesGroup):

    date = State()
    amount = State()
    category = State()

    input_stats_period = State()

@dp.message(isUser(), (F.text == "Добавить запись"))
@dp.message(isUser(), States.amount)
@dp.message(isUser(), States.category)
@dp.message(isUser(), States.date)
async def adding_entry(message: types.Message, state: FSMContext):
    
    current_state = await state.get_state()

    if not current_state:
        
        await state.update_data(type=message.text)
        await message.answer("Выберите день: ", reply_markup=keyboard("Сегодня", "Вчера", "Отмена"))
        await state.set_state(States.date)

    elif message.text == "Отмена":

        await state.clear()

        await message.answer("Запись удалена!", reply_markup=keyboard("Добавить запись", "Удалить запись", "Статистика")) 

    elif current_state == States.date.state:

        if message.text == "Сегодня": date = datetime.now().strftime(Settings().format.datetime)
        elif message.text == "Вчера": date = (datetime.now() - timedelta(days=1)).strftime(Settings().format.datetime)

        await state.update_data(date=date)
        await message.answer("Введите сумму: ", reply_markup=keyboard("Отмена"))
        await state.set_state(States.amount)

    elif current_state == States.amount.state:

        await state.update_data(amount=message.text)
        await message.answer("Введите категорию: ", reply_markup=keyboard(*[item.value for item in Transactions_Categories], "Отмена"))
        await state.set_state(States.category)

    elif current_state == States.category.state:

        await state.update_data(category=message.text)

        data = await state.get_data()

        transaction = Transaction(
            data['date'],
            data['amount'],
            data['category']
        )

        User(message.from_user.id, message.from_user.first_name).update(transaction)

        await state.clear()

        await message.answer("Запись добавлена!", reply_markup=keyboard("Добавить запись", "Удалить запись", "Статистика"))

@dp.message(isUser(), F.text == "Главное меню")
@dp.message(isUser(), Command('start'))
async def start_status_handler(message: Message, state: FSMContext):
    
    await state.clear()

    User(message.from_user.id, message.from_user.first_name)

    text = ("Бим бим бам бам\n\n"+
            "Скока заработави?")

    await message.answer(text, reply_markup = keyboard("Добавить запись", "Удалить запись", "Статистика"))

@dp.message(isUser(), F.text == "Удалить запись")
async def remove_entry(message: Message):

    #каждая запись - сообщение с кнопкой
    transactions = User(message.from_user.id, message.from_user.first_name).transactions

    if not transactions:
        await message.answer("Нет данных")
        return
    
    for t in transactions:

        mess = await message.answer(f"{t.datetime[5:10]} {t.category} {t.amount}р ")
        await mess.edit_reply_markup(str(mess.message_id), inline_keyboard(("Удалить", f"Remove/{t.datetime}/{mess.message_id}/{message.from_user.id}")))

@dp.callback_query(lambda query: query.data.startswith("Remove"))
async def removing_entry(query: CallbackQuery):

    data = query.data.split('/')

    await query.bot.delete_message(data[3], data[2])

    User(data[3], query.from_user.first_name).remove_transaction(data[1])

    await query.bot.send_message(data[3], "Запись удалена!", reply_markup = keyboard("Добавить запись", "Удалить запись", "Статистика"))

@dp.message(isUser(), F.text == "Статистика")
async def stats(message: Message):

    await message.answer("Выберите период:", reply_markup=keyboard("Месяц", "Все время","Ввести вручную", "Главное меню"))

@dp.message(isUser(), F.text == "Месяц")
async def stats_per_mounth(message: Message):

    await message.answer(Stats.per_month(message.from_user.id))

@dp.message(isUser(), F.text == "Все время")
async def stats_all_time(message: Message):

    await message.answer(Stats.all_time(message.from_user.id))

@dp.message(isUser(), F.text == "Ввести вручную")
async def await_stats_period(message: Message, state: FSMContext):

    await state.set_state(States.input_stats_period)

    await message.answer("Пример: с 05.05 по 03.06")

@dp.message(isUser(), States.input_stats_period)
async def stats_for_the_period(message: Message, state: FSMContext):

    await state.clear()

    dates = message.text.split()[1:4:2]

    d1 = datetime(year=datetime.now().year, month=int(dates[0].split(".")[1]), day=int(dates[0].split(".")[0])).strftime(Settings().format.datetime)
    d2 = datetime(year=datetime.now().year, month=int(dates[1].split(".")[1]), day=int(dates[1].split(".")[0]), hour=23, minute=59).strftime(Settings().format.datetime)


    await message.answer(Stats.for_the_period(message.from_user.id, d1, d2))










