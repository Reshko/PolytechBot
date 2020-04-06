import logging
import config
import re
from telegram import ReplyKeyboardMarkup
from keyboard import get_base_reply_keyboard
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.request import Request
from telegram import Bot


def debug_requests(f):
    '''Декоратор для отладки событий
    '''

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

########################################################################################################################
BUTTON1_LESSONS = "Расписание"
BUTTON2_ADDRESS = "Адрес"
BUTTON3_INFO = "Информация"

reply_keyboard = [
    [
        BUTTON1_LESSONS, BUTTON2_ADDRESS
    ]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


########################################################################################################################

@debug_requests
def do_start(update, context):
    update.message.reply_text(
        "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
        "Why don't you tell me something about yourself?",
        reply_markup=markup
    )


@debug_requests
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


@debug_requests
def echo(update: Updater, context):
    if update.message.text == BUTTON1_LESSONS:
        print(update.message)
        # update.message.reply_text("Введите учебную группу")
        # text2 = update.message.text
        # tpl = '\d\d\d[-]\d\d\d'
        # if re.match(tpl, text2) is not None:
        #     update.message.reply_text("Соответсвует")
        # else:
        #     update.message.reply_text('# Не соответствует')
    elif update.message.text == BUTTON2_ADDRESS:
        update.message.reply_text("Вот и адрес")


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

    # TODO подлючить бд и сделать декораторы

    # Default connection
    # updater = Updater(config.token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", do_start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
