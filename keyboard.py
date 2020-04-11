from telegram import ReplyKeyboardMarkup

#Инициация клавиатуры
BUTTON1_LESSONS = "Расписание"
BUTTON2_ADDRESS = "Адрес"

reply_keyboard = [
    [
        BUTTON1_LESSONS, BUTTON2_ADDRESS
    ]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True) #one_time_keyboard - клава закрывается после нажатия,resize_keyboard - маленькие кнопки