from telegram import ReplyKeyboardMarkup

#Инициация клавиатуры
BUTTON1_LESSONS = "Расписание"
BUTTON2_ADDRESS = "Адрес"

BUTTON3_ELECTRO = "Электрозаводская"
BUTTON4_AVTO = "Автозаводская"
BUTTON4_VPNH = "ВДНХ"

reply_keyboard = [
    [
        BUTTON1_LESSONS, BUTTON2_ADDRESS
    ]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True) #one_time_keyboard - клава закрывается после нажатия,resize_keyboard - маленькие кнопки

reply_keyboard2 = [
    [
        BUTTON3_ELECTRO
    ],
    [
        BUTTON4_AVTO,BUTTON4_VPNH
    ]
]

markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True, resize_keyboard=True)