import sys
import threading
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

import config
import telegram

module = sys.modules[__name__]
module.messages_queue = []


def process_messages_queue():
    while True:
        i = 0
        for message in module.messages_queue:
            if message.text == '':
                continue

            module.api.messages.send(peer_id=2000000000 + config.vk.get('chatId'), random_id=get_random_id(),
                                     message=message.from_user.first_name + ('' if message.from_user.last_name is None else ' ' + message.from_user.last_name) + ': ' + message.text)
            module.messages_queue.pop(i)
            i = i + 1


def handle_messages(long_poll):
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_chat and event.chat_id == config.vk.get('chatId'):
            telegram.messages_queue.insert(0, [event, module.api.users.get(user_ids=event.user_id)])


def init():
    vk_session = vk_api.VkApi(config.vk.get('login'), config.vk.get('password'), app_id=2685278)
    vk_session.auth(token_only=True)

    module.api = vk_session.get_api()

    long_poll = VkLongPoll(vk_session)

    t1 = threading.Thread(target=handle_messages, args=[long_poll])
    t2 = threading.Thread(target=process_messages_queue)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
