from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='My notes')
        ],
        [
            KeyboardButton(text='Add note'),
        ],
        [
            KeyboardButton(text='Change timezone')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

note_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Edit note'),
            KeyboardButton(text='Delete note'),
        ],
        [
            KeyboardButton(text='❌')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

edit_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Edit note name'),
            KeyboardButton(text='Edit note description'),
        ],
        [
            KeyboardButton(text='Edit note notification time'),
        ],
        [
            KeyboardButton(text='❌')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

timezone_continent_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Europe')],
        [KeyboardButton(text='America')],
        [KeyboardButton(text='Asia')],
        [KeyboardButton(text='Africa')],
        [KeyboardButton(text='Australia')],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)
