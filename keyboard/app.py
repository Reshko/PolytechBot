from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import db
import keyboard.MainKeyboard
import keyboard.KeyboardInline

markup = ReplyKeyboardMarkup(keyboard.MainKeyboard.main_keyboard, one_time_keyboard=True, resize_keyboard=True) #one_time_keyboard - клава закрывается после нажатия,resize_keyboard - маленькие кнопки

inline_markup = InlineKeyboardMarkup(keyboard.KeyboardInline.inline_keyboard)

inline_markup2 = InlineKeyboardMarkup(keyboard.KeyboardInline.inline_keyboard2)

inline_markup_info = InlineKeyboardMarkup(keyboard.KeyboardInline.inline_keyboard3)

inline_markup_admin = InlineKeyboardMarkup(keyboard.KeyboardInline.admin_keyboard)

inline_markup_manager = InlineKeyboardMarkup(keyboard.KeyboardInline.managet_keyboard)

inline_markup_tester = InlineKeyboardMarkup(keyboard.KeyboardInline.tester_keyboard)

inline_markup_database_tester = InlineKeyboardMarkup(keyboard.KeyboardInline.database_tester_keyboard)









