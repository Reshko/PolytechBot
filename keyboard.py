from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

#Инициация клавиатуры
BUTTON1_LESSONS = "Расписание"
BUTTON2_ADDRESS = "Адрес"
BUTTON_INFO = "Контактная информация"

BUTTON3_ELECTRO = "Электрозаводская"
BUTTON4_AVTO = "Автозаводская"
BUTTON4_VPNH = "ВДНХ"

reply_keyboard = [
    [
        BUTTON1_LESSONS, BUTTON2_ADDRESS
    ],
    [
        BUTTON_INFO
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

inline_keyboard = [[InlineKeyboardButton(BUTTON3_ELECTRO, callback_data=str(BUTTON3_ELECTRO)),
              InlineKeyboardButton(BUTTON4_AVTO, callback_data=str(BUTTON4_AVTO))],

             [InlineKeyboardButton(BUTTON4_VPNH, callback_data=str(BUTTON4_VPNH))]]

inline_markup = InlineKeyboardMarkup(inline_keyboard)

inline_keyboard2 = [[InlineKeyboardButton("Назад")]

]