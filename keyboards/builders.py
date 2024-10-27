from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
import pytz

def notesKb(notes):
    builder = ReplyKeyboardBuilder()

    for n in notes:
        builder.add(KeyboardButton(text=n))
    builder.add(KeyboardButton(text='❌'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def timezoneCityKb(continent):
    timezones = [tz for tz in pytz.all_timezones if f'{continent}/' in tz]
    builder = ReplyKeyboardBuilder()

    for n in timezones:
        builder.add(KeyboardButton(text=n))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)