import logging

from dotenv import load_dotenv
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters
from os import getenv
from functools import partial

from handler import TelegramHandler
from get_dialogflow_answer import get_answer


logger = logging.getLogger('TelegramHandler')


def send_message(session_id, project_id, update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    answer, fallback = get_answer(user_message, session_id, project_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    logger.info(f'TG bot\nUser: {user_message}\nFallback: {fallback}\nBot: {answer}')


def main():
    load_dotenv()
    token = getenv('TG_TOKEN')
    session_id = getenv('TG_CHAT_ID')
    project_id = getenv('DIALOG_FLOW_PROJECT_ID')

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramHandler())
    logger.info('Telegram bot started')

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, partial(send_message, session_id, project_id)))

    updater.start_polling()


if __name__ == '__main__':
    main()
