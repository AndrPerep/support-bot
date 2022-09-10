import random
import vk_api as vk

from dotenv import load_dotenv
from os import getenv
from vk_api.longpoll import VkLongPoll, VkEventType

from get_dialogflow_answer import get_answer


def send_message(event, vk_api):
    answer, fallback = get_answer(event.text, event.user_id)
    if not fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':
    load_dotenv()
    vk_token = getenv('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_message(event, vk_api)
