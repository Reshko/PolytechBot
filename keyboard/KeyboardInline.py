from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import db

BUTTON_ELECTRO = "Электрозаводская"
BUTTON_AVTO = "Автозаводская"
BUTTON_VPNH = "ВДНХ"

inline_keyboard = [
    [
        InlineKeyboardButton(BUTTON_ELECTRO, callback_data=str(BUTTON_ELECTRO)), InlineKeyboardButton(BUTTON_AVTO, callback_data=str(BUTTON_AVTO))
    ],
    [
        InlineKeyboardButton(BUTTON_VPNH, callback_data=str(BUTTON_VPNH))
    ]
]

BUTTON_PREV = "◀"
BUTTON_NEXT = "▶"
BUTTON_ALL_DAY = "На всю неделю"

inline_keyboard2 = [
    [
        InlineKeyboardButton(BUTTON_PREV,callback_data="Prev"), InlineKeyboardButton(BUTTON_NEXT,callback_data="Next")
    ],
    [
        InlineKeyboardButton(BUTTON_ALL_DAY,callback_data="AllLessons")
    ]
]

inline_keyboard3 = [
        [
            InlineKeyboardButton("Приёмная коммиссия", callback_data="Приёмная коммиссия")
        ],
        [
            InlineKeyboardButton("LMS",url="https://lms.mospolytech.ru/"),InlineKeyboardButton("Личный \t Кабинет",url="https://e.mospolytech.ru/")
        ],
        [
            InlineKeyboardButton("Профком", callback_data="Профком"),InlineKeyboardButton("ЦРС", callback_data="ЦРС")
        ],
        [
            InlineKeyboardButton("Бугалтерия", callback_data="Бугалтерия")
        ]
]

def get_url_address(name_address :str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Карта",url=str(db.get_url_address(name_address)))
            ],
            [
                InlineKeyboardButton(BUTTON_ELECTRO, callback_data=str(BUTTON_ELECTRO)),InlineKeyboardButton(BUTTON_VPNH, callback_data=str(BUTTON_VPNH))
            ],
            [
                InlineKeyboardButton(BUTTON_AVTO, callback_data=str(BUTTON_AVTO))
            ],
        ]
    )