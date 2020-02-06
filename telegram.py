import sys
import threading
import telebot

import config
import vk

module = sys.modules[__name__]
module.messages_queue = []


def process_messages_queue():
    while True:
        i = 0
        for message in module.messages_queue:
            if message[0].text == '':
                continue

            module.api.send_message(config.telegram.get('chatId'),
                                    message[1][0]['first_name'] + ' ' + message[1][0]['last_name'] + ':\n' + message[0].text)
            module.messages_queue.pop(i)
            i = i + 1


def handle_messages(messages):
    for message in messages:
        if message.content_type == 'text' and message.from_user.is_bot is False and message.chat.id == config.telegram.get('chatId'):
            vk.messages_queue.insert(0, message)


def init():
    module.api = telebot.TeleBot(config.telegram.get('token'))
    module.api.set_update_listener(handle_messages)

    t1 = threading.Thread(target=module.api.polling)
    t2 = threading.Thread(target=process_messages_queue)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
