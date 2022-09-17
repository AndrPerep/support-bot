import random
import vk_api as vk
import logging
import telegram

from dotenv import load_dotenv
from os import getenv
from vk_api.longpoll import VkLongPoll, VkEventType

from get_dialogflow_answer import get_answer


logger = logging.getLogger('TelegramHandler')


def send_message(event, vk_api):
    user_message = event.text
    answer, fallback = get_answer(user_message, event.user_id)
    if not fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )
    logger.info(f'VK bot\nUser: {user_message}\nFallback: {fallback}\nBot: {answer}')


def main():
    load_dotenv()

    admin_bot = telegram.Bot(getenv('ADMIN_BOT_TOKEN'))
    admin_tg_chat_id = getenv('ADMIN_CHAT_ID')
    vk_token = getenv('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    class TelegramHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            admin_bot.send_message(chat_id=admin_tg_chat_id, text=log_entry)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramHandler())
    logger.info('Telegram bot started')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_message(event, vk_api)


if __name__ == '__main__':
    main()
