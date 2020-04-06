from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

BUTTON1_LESSONS = "Расписание"
BUTTON2_ADDRESS = "Адрес"



reply_keyboard = [
    [
        BUTTON1_LESSONS,BUTTON2_ADDRESS
    ]
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON1_LESSONS),
            KeyboardButton(BUTTON2_ADDRESS)
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )