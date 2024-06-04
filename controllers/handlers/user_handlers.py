from ..keyboards import *
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from ..keyboards.keyboards import *
from aiogram.dispatcher.filters import Text
from ..filters.main_filter import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from models import Transaction, Transactions_Categories, User
from stats import Stats
from datetime import datetime, timedelta


class States(StatesGroup):

    date = State()
    amount = State()
    category = State()

    input_stats_period = State()

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


async def start_status_handler(message: Message, state: FSMContext):
    
    await state.reset_state(with_data=True)

    User(message.from_id, message.from_user.first_name)

    text = ("Бим бим бам бам\n\n"+
            "Скока заработави?")

    await message.answer(text, reply_markup = keyboard("Добавить запись", "Удалить запись", "Статистика"))

async def remove_entry(message: Message):

    #каждая запись - сообщение с кнопкой
    transactions = User(message.from_id, message.from_user.first_name).transactions

    if not transactions:
        await message.answer("Нет данных")
        return
    
    for t in transactions:

        mess = await message.answer(f"{t.datetime[:5]} {t.category} {t.amount}р ")
        await mess.edit_reply_markup(inline_keyboard(("Удалить", f"Remove/{t.datetime}/{mess.message_id}/{message.from_id}")))


async def removing_entry(query: CallbackQuery):

    data = query.data.split('/')

    await query.bot.delete_message(data[3], data[2])

    User(data[3], query.from_user.first_name).remove_transaction(data[1])

    await query.bot.send_message(data[3], "Запись удалена!", reply_markup = keyboard("Добавить запись", "Удалить запись", "Статистика"))

async def stats(message: Message):

    await message.answer("Выберите период:", reply_markup=keyboard("Месяц", "Все время","Ввести вручную"))

async def stats_per_mounth(message: Message):

    await message.answer(Stats.per_month(message.from_id))

async def stats_all_time(message: Message):

    await message.answer(Stats.all_time(message.from_id))

async def await_stats_period(message: Message):

    await States.input_stats_period.set()

    await message.answer("Пример: с 05.05 по 03.06")

async def stats_for_the_period(message: Message, state: FSMContext):

    await state.reset_state(with_data=True)

    dates = message.text.split()[1:4:2]

    d1 = datetime(year=datetime.now().year, month=int(dates[0].split(".")[1]), day=int(dates[0].split(".")[0])).strftime(Settings().format.datetime)
    d2 = datetime(year=datetime.now().year, month=int(dates[1].split(".")[1]), day=int(dates[1].split(".")[0]), hour=23, minute=59).strftime(Settings().format.datetime)


    await message.answer(Stats.for_the_period(message.from_id, d1, d2))

def register_user_handlers(dp: Dispatcher):

    dp.register_message_handler(start_status_handler, isUser(), commands=['start'])
    dp.register_message_handler(adding_entry, isUser(), Text(equals=("Добавить запись")))
    dp.register_message_handler(remove_entry, isUser(), Text(equals=("Удалить запись")))
    dp.register_message_handler(adding_entry, isUser(), state=States.amount)
    dp.register_message_handler(adding_entry, isUser(), state=States.category)
    dp.register_message_handler(adding_entry, isUser(), state=States.date)
    dp.register_message_handler(stats, isUser(), Text(equals=("Статистика")))
    dp.register_message_handler(stats_per_mounth, isUser(), Text(equals=("Месяц")))
    dp.register_message_handler(stats_all_time, isUser(), Text(equals=("Все время")))
    dp.register_message_handler(await_stats_period, isUser(), Text(equals=("Ввести вручную")))
    dp.register_message_handler(stats_for_the_period, isUser(), state=States.input_stats_period)


    dp.register_callback_query_handler(removing_entry, lambda query: query.data.startswith("Remove"))










