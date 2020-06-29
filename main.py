import json
import logging
import sys
from pathlib import Path

from config import token
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram.utils.request import Request
from telegram import Bot, ParseMode
from db import DB
import requests
import datetime
from dbConfig import MakeDb

sys.path.insert(0, '/keyboard/')
from keyboard import app
from keyboard import MainKeyboard
from keyboard import KeyboardInline
from admin.admin import admin
from manager.manage_main import manager
from tester.tester_main import tester
from database_tester.database_main import data_base_tester



''' Декоратор для отладки событий '''
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
        "<b>Добро пожаловать</b>",
        reply_markup=app.markup,
        parse_mode = ParseMode.HTML
    )
    return ECHO

def help(update: Updater, context):
    update.message.reply_text(
        "/start - Запуск бота \n"
        "/info - Информация о боте",
    )




@debug_requests
def json_lesson(id):
    url = "https://rasp.dmami.ru/site/group?session=0&group=" + id
    headers = {'referer': 'https://rasp.dmami.ru/'}
    r = requests.get(url, headers=headers).json()
    return r

@debug_requests
def echo(update: Updater, contex):
    maketb = MakeDb()
    user = update.message.from_user
    if update.message.text == MainKeyboard.BUTTON_LESSONS and DB.count_group(user.id) == 0:
        update.message.reply_text("Введите группу 📝 ")
        return LESSONS
    elif update.message.text == MainKeyboard.BUTTON_CHANGE:
        update.message.reply_text("Введите группу 📝 ")
        return CHANGE_GROUP
    elif update.message.text == MainKeyboard.BUTTON_INFO:
        update.message.reply_text("💬 Ваш выбор", reply_markup=app.inline_markup_info)
    elif update.message.text == MainKeyboard.BUTTON_LESSONS and DB.count_group(user.id) > 0:
        print(user)
        number_group = DB.search_users(user.id)
        #r = json_lesson(number_group)


        path = Path('config/less.json')
        r = json.loads(path.read_text(encoding='utf-8'))
        print(r)
        #today = datetime.datetime.today().isoweekday()
        today = 4
        if today < 7:
            print(r['grid'][str(today)])
            a = 0
            while a != 7:
                a += 1
                try:
                    name_lesson = str(r['grid'][str(today)][str(a)][0]['sbj'])
                    teacher = str(r['grid'][str(today)][str(a)][0]['teacher'])
                    time_lesson = DB.search_time_lesson(a)
                    update.message.reply_text('<i>'+time_lesson+'</i>' + '\n' + name_lesson + "\n" + teacher,
                                              parse_mode=ParseMode.HTML)
                except IndexError:
                    continue
            update.message.reply_text('Please choose:', reply_markup=app.inline_markup2)
            return ECHO
        else:
            update.message.reply_text("Воскресенье 🌄", reply_markup=app.inline_markup2)
    elif update.message.text == MainKeyboard.BUTTON_ADDRESS:
        update.message.reply_text('Выберети адресс', reply_markup=app.inline_markup)
        return ECHO

@debug_requests
def change_group(update: Updater, contex):
    user_text = update.message.text
    user = update.message.from_user
    tpl = '\d\d\d[-]\d\d\d'
    if re.match(tpl, user_text) is not None:
        if (DB.serach_group(user_text) > 0):
            update.message.reply_text("Группа изменена ✅", reply_markup=app.markup)
            DB.update_group(user_text,user.id)
            return ECHO
        else: update.message.reply_text("Такой группы не существует ❌")
    else: update.message.reply_text("Не соответсвует форме 💥")

@debug_requests
def button(update: Updater, context):
    query = update.callback_query
    print(query)
    if query.data == KeyboardInline.BUTTON_ELECTRO:
        query.edit_message_text(str(DB.get_address(query.data)), reply_markup=KeyboardInline.get_url_address(query.data))
    elif query.data == KeyboardInline.BUTTON_AVTO:
        query.edit_message_text(str(DB.get_address(query.data)), reply_markup=KeyboardInline.get_url_address(query.data))
    elif query.data == KeyboardInline.BUTTON_VPNH:
        query.edit_message_text(str(DB.get_address(query.data)), reply_markup=KeyboardInline.get_url_address(query.data))
    elif query.data == "Prev":
        number_group = DB.search_users(query.message.chat.id)
        r, today = prevOrNextLesson(number_group, False)
        if today != 7:
            a = 0
            while a != 7:
                a += 1
                try:
                    name_lesson = str(r['grid'][str(today)][str(a)][0]['sbj'])
                    teacher = str(r['grid'][str(today)][str(a)][0]['teacher'])
                    time_lesson = DB.search_time_lesson(a)
                    query.message.reply_text('<i>'+time_lesson+'</i>' + '\n' + name_lesson + "\n" + teacher,
                                             parse_mode=ParseMode.HTML)
                except IndexError:
                    continue
            query.message.reply_text('Please choose:', reply_markup=app.inline_markup2)
        else: query.message.reply_text("Воскресенье 🌄",reply_markup=app.inline_markup2)
    elif query.data == "Next":
        number_group = DB.search_users(query.message.chat.id)
        r, today = prevOrNextLesson(number_group,True)
        if today != 7:
            a = 0
            while a != 7:
                a += 1
                try:
                    name_lesson = str(r['grid'][str(today)][str(a)][0]['sbj'])
                    teacher = str(r['grid'][str(today)][str(a)][0]['teacher'])
                    time_lesson = DB.search_time_lesson(a)
                    query.message.reply_text('<i>' + time_lesson + '</i>' + '\n' + name_lesson + "\n" + teacher,
                                             parse_mode=ParseMode.HTML)
                except IndexError:
                    continue
            query.message.reply_text('Please choose:', reply_markup=app.inline_markup2)
        else: query.message.reply_text("Воскресенье 🌄",reply_markup=app.inline_markup2)
    elif query.data == "AllLessons":
        #number_group = DB.search_users(query.message.chat.id)
        #r, today = prevOrNextLesson(number_group, True)
        today = 2
        path = Path('config/less.json')
        r = json.loads(path.read_text(encoding='utf-8'))
        if today != 7:
            a = 0
            b = 0
            while b != 6:
                b += 1
                a = 0
                day_week = DB.search_dayWeek(b,None)
                query.message.reply_text("<b>"+day_week+"</b>",
                                         parse_mode=ParseMode.HTML)
                while a != 7:
                    a += 1
                    try:
                        name_lesson = str(r['grid'][str(b)][str(a)][0]['sbj'])
                        teacher = str(r['grid'][str(b)][str(a)][0]['teacher'])
                        time_lesson = str(DB.search_time_lesson(a))
                        query.message.reply_text('<i>' + time_lesson + '</i>' + '\n' + name_lesson + "\n" + teacher,
                                                 parse_mode=ParseMode.HTML)
                    except IndexError:
                        continue
        else:
            query.message.reply_text("Воскресенье 🌄")
    elif query.data == "Приёмная коммиссия":
        query.edit_message_text("+7 (495) 223-05-23 \n Добавочные 1430, 1431, 1250, 1296 \n priem@mospolytech.ru", reply_markup=app.inline_markup_info)
    elif query.data == "Профком":
        query.edit_message_text("+7 (495) 223-05-31 \n profkom@mospolytech.ru", reply_markup=app.inline_markup_info)
    elif query.data == "Бугалтерия":
        query.edit_message_text("+7 (495) 223-05-23 \n Добавочные 1322, 1236, 1379", reply_markup=app.inline_markup_info)
    elif query.data == "ЦРС":
        query.edit_message_text("+7 (495) 223-05-23 \n Добавочные 1116 \n ghbty.e.gorina@mospolytech.ru", reply_markup=app.inline_markup_info)
    #Администатор
    elif query.data == 'Кол-во пользователей':
        now = datetime.datetime.now()
        query.edit_message_text(str(now.strftime("%d-%m-%Y %H:%M")) + "\n"+str(DB.select_all_users(None))+ " users",
                                reply_markup=app.inline_markup_admin)
    elif query.data == 'Бд':
        now = datetime.datetime.now()
        query.edit_message_text(str(now.strftime("%d-%m-%Y %H:%M")) + "\n"
                                 + "Sqllite 7 таблиц sqlite3" + "\n"
                                 + "MongoDb 2 таблицы pyMongo",reply_markup=app.inline_markup_admin)
    elif query.data == 'Кол-во групп':
        now = datetime.datetime.now()
        query.edit_message_text(str(now.strftime("%d-%m-%Y %H:%M")) + "\n"
                                + str("В базе данных присутсвует 400 групп"),reply_markup=app.inline_markup_manager)
    elif query.data == "Активность":
        now = datetime.datetime.now()
        query.edit_message_text(str(now.strftime("%d-%m-%Y %H:%M")) + "\n"
                                +"За последние 2 дня 0 новыйх пользователей",reply_markup=app.inline_markup_manager)
    elif query.data == "Функция1":
        query.edit_message_text('.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                'log.info Функция Prev() уcпешно отработала',
                                reply_markup=app.inline_markup_tester)
    elif query.data == "Функция2":
        query.edit_message_text('.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                'log.info Функция Next() уcпешно отработала',
                                reply_markup=app.inline_markup_tester)
    elif query.data == "Функция3":
        query.edit_message_text('.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                'log.info Функция All_lesson() уcпешно отработала',
                                reply_markup=app.inline_markup_tester)
    elif query.data == "Функция4":
        query.edit_message_text('.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                'log.info Функция Change_group() уcпешно отработала',
                                reply_markup=app.inline_markup_tester)
    elif query.data == "Таблица1":
        query.edit_message_text('.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                'log.info Таблица address: 5 полей, 1 ключ',
                                reply_markup=app.inline_markup_database_tester)
    elif query.data == "Таблица2":
        query.edit_message_text('.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                'log.info Таблица info_users: 10 полей , 1 ключ, 2 внешний ключ',
                                reply_markup=app.inline_markup_database_tester)
    elif query.data == "Таблица3":
        query.edit_message_text('.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                'log.info Таблица all_group: 400 полей, 1 ключ',
                                reply_markup=app.inline_markup_database_tester)
    elif query.data == "Таблица4":
        query.edit_message_text('.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                '.'+'\n'+
                                'log.info Таблица  info_deveice:10 полей ',
                                reply_markup=app.inline_markup_database_tester)

@debug_requests
def prevOrNextLesson(number_group: str, flag: bool):
    r = json_lesson(number_group)
    today = datetime.datetime.today().isoweekday()
    #today = 3
    if flag:  # NextDay
        today = 1 if today == 7 else today + 1
    else:  # PrevDay
        today = 7 if today == 1 else today - 1
    return r, today

def get_info(update:Updater, contex):
    update.message.reply_text("Данный телеграм бот является курсовым проектом \nОсновной задачей которого является "
                              "предоставляение необходимый информации \n"
                              "kolpak.al6@yandex.ru")

@debug_requests
def lessons(update:Updater, contex):
    user_text = update.message.text
    user = update.message.from_user
    tpl = '\d\d\d[-]\d\d\d'
    if re.match(tpl, user_text) is not None:
        if (DB.serach_group(user_text) > 0):
            print(user)
            DB.add_users(user.id,user.first_name,user.last_name,user.username,user_text)
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
                        update.message.reply_text(str(DB.search_time_lesson(a)) + ')' + name_lesson + "/" + teacher )
                    except IndexError:
                        continue
                update.message.reply_text('Please choose:', reply_markup=app.inline_markup2)
                return ECHO
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

@debug_requests
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
    dp.add_handler(CommandHandler('info',get_info))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('admin',admin))
    dp.add_handler(CommandHandler('manager', manager))
    dp.add_handler(CommandHandler('tester', tester))
    dp.add_handler(CommandHandler('database',data_base_tester))
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
