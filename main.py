import json
import logging
import config
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.utils.request import Request
from telegram import Bot
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

@debug_requests
def echo(update:Updater, contex):
    user = update.message.from_user
    if update.message.text == keyboard.BUTTON1_LESSONS and db.count_group(user.id) == 0:
        update.message.reply_text("Введи группу")
        return LESSONS
    elif update.message.text == keyboard.BUTTON1_LESSONS and db.count_group(user.id) > 0:
        number_group = db.search_users(user.id)
        print('Старый пользователь')
        url = "https://rasp.dmami.ru/site/group?session=0&group=" + number_group
        headers = {'referer': 'https://rasp.dmami.ru/'}
        r = requests.get(url, headers=headers)
        print(r.status_code)
        r = r.json()
        today = datetime.datetime.today().isoweekday()
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
                update.message.reply_text(str(a) + ')' + name_lesson + "/" + teacher)

            except IndexError:
                continue

        update.message.reply_text("Изменить группу")
    elif update.message.text == keyboard.BUTTON2_ADDRESS:
        update.message.reply_text("Выбири адрес")
        return ADDRESS
    else:
        update.message.reply_text("Я не знаю(")


#TODO Сделать функцию вывода рассписания
@debug_requests
def printLessons(text_group):
    return 1


@debug_requests
def lessons(update:Updater, contex):
    user_text = update.message.text
    tpl = '\d\d\d[-]\d\d\d'
    if re.match(tpl, user_text) is not None:
        update.message.reply_text("Соответствует форме")
        if (db.serach_group(user_text) > 0):
            update.message.reply_text("Группа есть")
            url = "https://rasp.dmami.ru/site/group?session=0&group=" + user_text
            headers = {'referer': 'https://rasp.dmami.ru/'}
            r = requests.get(url, headers=headers)
            print(r.status_code)
            r = r.json()
            today = datetime.datetime.today().isoweekday()
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
                    update.message.reply_text(str(a) + ')' + name_lesson + "/" + teacher )

                except IndexError:
                    continue

        else:
            update.message.reply_text("Такой группы не существует")
    else:
        update.message.reply_text("Не соответствует")

@debug_requests
def address(update:Updater, contex):
    update.message.reply_text("ты в адрессе")

@debug_requests
def cancel(update, context):
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

    # TODO подлючить бд


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', do_start)],

        states={

            ECHO:[MessageHandler(Filters.text, echo)],

            LESSONS: [MessageHandler(Filters.text, lessons)],

            ADDRESS: [MessageHandler(Filters.text, address)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # on different commands - answer in Telegram
    #dp.add_handler(CommandHandler("start", do_start))
    dp.add_handler(CommandHandler("help", help))
    #dp.add_handler(MessageHandler(Filters.text, echo))
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
