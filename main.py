import logging
from config import token
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram.utils.request import Request
from telegram import Bot
import db
import requests
import datetime
from keyboard import keyboard

'''Декоратор для отладки событий
  '''
def debug_requests(f):
    def inner(*args, **kwargs):
        try:
            logger.info(f"Обращение в функцию {f.__name__}")
            return f(*args, **kwargs)
        except Exception:
            logger.exception(f"Ошибка в обработчике {f.__name__}")
            raise
    return inner

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

ECHO, LESSONS, CHANGE_GROUP = range(3)

@debug_requests
def do_start(update: Updater, context):
    update.message.reply_text(
        "Всем привет",
        reply_markup=keyboard.markup
    )
    return ECHO

def json_lesson(id):
    url = "https://rasp.dmami.ru/site/group?session=0&group=" + id
    headers = {'referer': 'https://rasp.dmami.ru/'}
    r = requests.get(url, headers=headers).json()
    return r

@debug_requests
def echo(update: Updater, contex):
    user = update.message.from_user
    if update.message.text == keyboard.BUTTON1_LESSONS and db.count_group(user.id) == 0:
        update.message.reply_text("Введи группу")
        return LESSONS
    elif update.message.text == keyboard.BUTTON_CHANGE:
        update.message.reply_text("Введите группу")
        return CHANGE_GROUP
    elif update.message.text == keyboard.BUTTON_INFO:
        update.message.reply_text("💬 Ваш выбор", reply_markup=keyboard.inline_markup_info)
    elif update.message.text == keyboard.BUTTON1_LESSONS and db.count_group(user.id) > 0:
        print(user)
        number_group = db.search_users(user.id)
        r = json_lesson(number_group)
        today = datetime.datetime.today().isoweekday()
        if today < 7:
            print(r['grid'][str(today)])
            a = 0
            today_lessons = []
            while a != 7:
                a += 1
                try:
                    name_lesson = str(r['grid'][str(today)][str(a)][0]['sbj'])
                    teacher = str(r['grid'][str(today)][str(a)][0]['teacher'])
                    update.message.reply_text(str(db.search_time_lesson(a)) + ')' + name_lesson + "\n" + teacher)
                except IndexError:
                    continue
            update.message.reply_text('Please choose:', reply_markup=keyboard.inline_markup2)
            return ECHO
        else:
            update.message.reply_text("Воскресенье", reply_markup=keyboard.inline_markup2)
    elif update.message.text == keyboard.BUTTON2_ADDRESS:
        update.message.reply_text('Выберети адресс', reply_markup=keyboard.inline_markup)
        return ECHO

@debug_requests
def change_group(update: Updater, contex):
    user_text = update.message.text
    user = update.message.from_user
    tpl = '\d\d\d[-]\d\d\d'
    if re.match(tpl, user_text) is not None:
        if (db.serach_group(user_text) > 0):
            update.message.reply_text("Группа изменена", reply_markup=keyboard.markup)
            db.update_group(user_text,user.id)
            return ECHO
        else: update.message.reply_text("Такой группы не существует")
    else: update.message.reply_text("Не соответсвует форме")

@debug_requests
def button(update: Updater, context):
    query = update.callback_query

    if query.data == keyboard.BUTTON3_ELECTRO:
        query.edit_message_text(str(db.get_address(query.data)), reply_markup=keyboard.get_url_address(query.data))
    elif query.data == keyboard.BUTTON4_AVTO:
        query.edit_message_text(str(db.get_address(query.data)), reply_markup=keyboard.get_url_address(query.data))
    elif query.data == keyboard.BUTTON5_VPNH:
        query.edit_message_text(str(db.get_address(query.data)), reply_markup=keyboard.get_url_address(query.data))
    elif query.data == "Prev":
        number_group = db.search_users(query.message.chat.id)
        r, today = prevOrNextLesson(number_group, False)
        if today != 7:
            a = 0
            while a != 7:
                a += 1
                try:
                    name_lesson = str(r['grid'][str(today)][str(a)][0]['sbj'])
                    teacher = str(r['grid'][str(today)][str(a)][0]['teacher'])
                    query.message.reply_text(str(db.search_time_lesson(a)) + ')' + name_lesson + "/" + teacher )
                except IndexError:
                    continue
        else: query.message.reply_text("Воскресенье")
    elif query.data == "Next":
        number_group = db.search_users(query.message.chat.id)
        r, today = prevOrNextLesson(number_group,True)
        if today != 7:
            a = 0
            while a != 7:
                a += 1
                try:
                    name_lesson = str(r['grid'][str(today)][str(a)][0]['sbj'])
                    teacher = str(r['grid'][str(today)][str(a)][0]['teacher'])
                    query.message.reply_text(str(db.search_time_lesson(a)) + ')' + name_lesson + "/" + teacher )
                except IndexError:
                    continue
        else: query.message.reply_text("Воскресенье")
    elif query.data == "AllLessons":
        number_group = db.search_users(query.message.chat.id)
        r, today = prevOrNextLesson(number_group, True)
        if today != 7:
            a = 0
            b = 0
            while b != 6:
                b += 1
                a = 0
                query.message.reply_text(db.search_dayWeek(b))
                while a != 7:
                    a += 1
                    try:
                        name_lesson = str(r['grid'][str(b)][str(a)][0]['sbj'])
                        teacher = str(r['grid'][str(b)][str(a)][0]['teacher'])
                        query.message.reply_text(str(db.search_time_lesson(a)) + ')' + name_lesson + "/" + teacher)
                    except IndexError:
                        continue
        else:
            query.message.reply_text("Воскресенье")
    elif query.data == "Приёмная коммиссия":
        query.edit_message_text("+7 (495) 223-05-23 \n Добавочные 1430, 1431, 1250, 1296 \n priem@mospolytech.ru", reply_markup=keyboard.inline_markup_info)
    elif query.data == "Профком":
        query.edit_message_text("+7 (495) 223-05-31 \n profkom@mospolytech.ru", reply_markup=keyboard.inline_markup_info)
    elif query.data == "Бугалтерия":
        query.edit_message_text("+7 (495) 223-05-23 \n Добавочные 1322, 1236, 1379", reply_markup=keyboard.inline_markup_info)
    elif query.data == "ЦРС":
        query.edit_message_text("+7 (495) 223-05-23 \n Добавочные 1116 \n ghbty.e.gorina@mospolytech.ru", reply_markup=keyboard.inline_markup_info)

@debug_requests
def prevOrNextLesson(number_group: str, flag: bool):
    r = json_lesson(number_group)
    today = datetime.datetime.today().isoweekday()
    if flag:  # NextDay
        today = 1 if today == 7 else today + 1
    else:  # PrevDay
        today = 7 if today == 1 else today - 1
    return r, today

@debug_requests
def lessons(update:Updater, contex):
    user_text = update.message.text
    user = update.message.from_user
    tpl = '\d\d\d[-]\d\d\d'
    if re.match(tpl, user_text) is not None:
        update.message.reply_text("Соответствует форме")
        if (db.serach_group(user_text) > 0):
            print(user)
            db.add_users(user.id,user.first_name,user.last_name,user.username,user_text)
            r = json_lesson(user_text)
            today = datetime.datetime.today().isoweekday()
            print(today)
            if today < 7:
                print(r['grid'][str(today)])
                a = 0
                today_lessons = []
                while a != 7:
                    a += 1
                    try:
                        name_lesson = str(r['grid'][str(today)][str(a)][0]['sbj'])
                        today_lessons.append(name_lesson)
                        teacher = str(r['grid'][str(today)][str(a)][0]['teacher'])
                        today_lessons.append(teacher)
                        update.message.reply_text(str(db.search_time_lesson(a)) + ')' + name_lesson + "/" + teacher )

                    except IndexError:
                        continue
            else:
                update.message.reply_text("Сегодня нет пар")
        else:
            update.message.reply_text("Такой группы не существует")
    else:
        update.message.reply_text("Не соответствует")

@debug_requests
def cancel(update:Updater, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END

@debug_requests
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    logger.info("Start bot")

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0
    )

    bot = Bot(
        token=token.token,
        request=req
    )
    updater = Updater(
        bot=bot,
        use_context=True
    )

    info = bot.get_me()
    logger.info(f'Bot info: {info}')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', do_start)],

        states={

            ECHO:[MessageHandler(Filters.regex('^(Расписание|Адрес|Изменить группу|Контактная информация)$'), echo)],

            LESSONS: [MessageHandler(Filters.text, lessons)],

            CHANGE_GROUP: [MessageHandler(Filters.text, change_group)],

        },

        fallbacks=[CommandHandler('start', do_start)]
    )

    dp.add_handler(conv_handler)
    #updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CallbackQueryHandler(button))


    # dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
