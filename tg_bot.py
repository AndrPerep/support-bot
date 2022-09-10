import telegram
from telegram.error import NetworkError, Unauthorized

from time import sleep
from dotenv import load_dotenv
from os import getenv

from get_dialogflow_answer import get_answer

update_id = None


def start_bot():
    global update_id

    load_dotenv()
    tg_token = getenv('TG_TOKEN')
    bot = telegram.Bot(tg_token)

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
            answer, fallback = get_answer(update.message.text, session_id)
            print(update.message.text)
            update.message.reply_text(answer)


if __name__ == '__main__':
    start_bot()
