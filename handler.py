import logging

from os import getenv
from telegram import Bot


class TelegramHandler(logging.Handler):
    def emit(self, record):
        admin_bot = Bot(getenv('ADMIN_BOT_TOKEN'))
        admin_tg_chat_id = getenv('ADMIN_CHAT_ID')
        log_entry = self.format(record)
        admin_bot.send_message(chat_id=admin_tg_chat_id, text=log_entry)
