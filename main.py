import json
import logging
import config
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram.utils.request import Request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import db
import requests
import datetime
import keyboard

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

ECHO, LESSONS, ADDRESS = range(3)

@debug_requests
def do_start(update, context):
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
def echo(update:Updater, contex):
    user = update.message.from_user
    if update.message.text == keyboard.BUTTON1_LESSONS and db.count_group(user.id) == 0:
        update.message.reply_text("Введи группу")
        return LESSONS
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
                    today_lessons.append(name_lesson)
                    teacher = str(r['grid'][str(today)][str(a)][0]['teacher'])
                    today_lessons.append(teacher)
                    update.message.reply_text(str(db.search_time_lesson(a)) + ')' + name_lesson + "/" + teacher )
                except IndexError:
                    continue
            update.message.reply_text("Изменить группу")

            return ECHO
        else:
            update.message.reply_text("Воскресенье")
    elif update.message.text == keyboard.BUTTON2_ADDRESS:

        keyboard2 = [[InlineKeyboardButton(keyboard.BUTTON3_ELECTRO, callback_data='1'),
                     InlineKeyboardButton(keyboard.BUTTON4_AVTO, callback_data='2')],

                    [InlineKeyboardButton(keyboard.BUTTON4_VPNH, callback_data='3')]]

        reply_markup2 = InlineKeyboardMarkup(keyboard2)

        update.message.reply_text('Please choose:', reply_markup=reply_markup2)

        return ADDRESS

@debug_requests
def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))

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
def address(update:Updater, contex):
    if (update.message.text == 'Электрозаводская'):
        print()
    update.message.reply_text("ты в адрессе")

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
        token=config.token,
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

            ECHO:[MessageHandler(Filters.regex('^(Расписание|Адрес)$'), echo)],

            LESSONS: [MessageHandler(Filters.text, lessons)],

            ADDRESS: [MessageHandler(Filters.text, address)]

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(button))


    # dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
