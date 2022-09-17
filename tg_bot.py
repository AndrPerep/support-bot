import telegram
import logging

from time import sleep
from telegram.error import NetworkError, Unauthorized
from dotenv import load_dotenv
from os import getenv

from get_dialogflow_answer import get_answer


update_id = None
logger = logging.getLogger('TelegramHandler')


def main():
    global update_id

    load_dotenv()
    bot = telegram.Bot(getenv('TG_TOKEN'))
    admin_bot = telegram.Bot(getenv('ADMIN_BOT_TOKEN'))
    admin_tg_chat_id = getenv('ADMIN_CHAT_ID')

    class TelegramHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            admin_bot.send_message(chat_id=admin_tg_chat_id, text=log_entry)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramHandler())
    logger.info('Telegram bot started')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            send_message(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def send_message(bot):
    global update_id
    session_id = getenv('TG_CHAT_ID')
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # bot can receive updates without messages
            user_message = update.message.text
            answer, fallback = get_answer(update.message.text, session_id)
            update.message.reply_text(answer)
            logger.info(f'Telegram bot\nUser: {user_message}\nFallback: {fallback}\nBot: {answer}')


if __name__ == '__main__':
    main()
