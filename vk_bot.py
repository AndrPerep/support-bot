import random
import vk_api as vk
import logging
import telegram

from dotenv import load_dotenv
from os import getenv
from vk_api.longpoll import VkLongPoll, VkEventType

from handler import TelegramHandler
from get_dialogflow_answer import get_answer


logger = logging.getLogger('TelegramHandler')


def send_message(event, vk_api, project_id):
    user_message = event.text
    answer, fallback = get_answer(user_message, event.user_id, project_id)
    if not fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )
    logger.info(f'VK bot\nUser: {user_message}\nFallback: {fallback}\nBot: {answer}')


def main():
    load_dotenv()

    project_id = getenv('DIALOG_FLOW_PROJECT_ID')
    vk_token = getenv('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramHandler())
    logger.info('VK bot started')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_message(event, vk_api, project_id)


if __name__ == '__main__':
    main()
