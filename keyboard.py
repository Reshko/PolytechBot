from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import db

#Инициация клавиатуры
BUTTON1_LESSONS = "Расписание"
BUTTON_CHANGE = "Изменить группу"
BUTTON2_ADDRESS = "Адрес"
BUTTON_INFO = "Контактная информация"

BUTTON3_ELECTRO = "Электрозаводская"
BUTTON4_AVTO = "Автозаводская"
BUTTON5_VPNH = "ВДНХ"


BUTTON_PREV = "◀"
BUTTON_NEXT = "▶"
BUTTON_ALL_DAY = "На всю неделю"

reply_keyboard = [
    [
        BUTTON1_LESSONS, BUTTON2_ADDRESS
    ],
    [
        BUTTON_CHANGE
    ],
    [
        BUTTON_INFO
    ]
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True) #one_time_keyboard - клава закрывается после нажатия,resize_keyboard - маленькие кнопки

inline_keyboard = [
    [
        InlineKeyboardButton(BUTTON3_ELECTRO, callback_data=str(BUTTON3_ELECTRO)), InlineKeyboardButton(BUTTON4_AVTO, callback_data=str(BUTTON4_AVTO))
    ],
    [
        InlineKeyboardButton(BUTTON5_VPNH, callback_data=str(BUTTON5_VPNH))
    ]
]

inline_markup = InlineKeyboardMarkup(inline_keyboard)

def get_info(keyword: str):
    return InlineKeyboardMarkup(
        [
            []
        ]
    )

def get_url_address(name_address :str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Карта",url=str(db.get_url_address(name_address)))
            ],
            [
                InlineKeyboardButton(BUTTON3_ELECTRO, callback_data=str(BUTTON3_ELECTRO)),InlineKeyboardButton(BUTTON5_VPNH, callback_data=str(BUTTON5_VPNH))
            ],
            [
                InlineKeyboardButton(BUTTON4_AVTO, callback_data=str(BUTTON4_AVTO))
            ],
        ]
    )

inline_keyboard2 = [
    [
        InlineKeyboardButton(BUTTON_PREV,callback_data="Prev"), InlineKeyboardButton(BUTTON_NEXT,callback_data="Next")
    ],
    [
        InlineKeyboardButton(BUTTON_ALL_DAY,callback_data="AllLessons")
    ]
]

inline_markup2 = InlineKeyboardMarkup(inline_keyboard2)

