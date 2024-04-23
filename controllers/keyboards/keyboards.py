from aiogram import types



def keyboard(*args):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    for arg in args:

        keyboard.add(types.KeyboardButton(arg))

    return keyboard

def inline_keyboard(*args):
    """
    Принимает массив кортежей (текст кнопки, callback data)
    """
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for arg in args:

        keyboard.add(types.InlineKeyboardButton(arg[0], callback_data = arg[1]))

    return keyboard

