from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def keyboard(*args):


    # Создаем список списков с кнопками
    keyboard: list[list[KeyboardButton]] = []

    for arg in args:

        keyboard.append([KeyboardButton(text=arg)])

    # Создаем объект клавиатуры, добавляя в него кнопки
    my_keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


    return my_keyboard

def inline_keyboard(*args):
    """
    Принимает массив кортежей (текст кнопки, callback data)
    """
    
    builder = InlineKeyboardBuilder()

    for arg in args:

        builder.row(InlineKeyboardButton(text=arg[0], callback_data=arg[1]))


    return builder.as_markup()
