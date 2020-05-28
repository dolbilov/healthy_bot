'''
Healthy Bot
v 0.0.4-b
(c) Dolbilov Kirill 2020
'''

import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from time import sleep
from random import randint
from datetime import datetime
from config import *


vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, group_id=groupID)
vk = vk_session.get_api()

msg = 'Выпрями спину! <3'
att = 'photo136170463_'
num = 457259955
ids = '377010517, 113354166, 203338171, 136170463'


def send_msg(onlineIDs):
    vk_session.method('messages.send', {'message': msg,
                                        'random_id': get_random_id(),
                                        'user_ids': onlineIDs,
                                        'attachment': att + str(num + randint(0,49))
    })

while (True):
    a = vk_session.method('users.get', {'user_ids': ids,
                                    'fields': 'online'
    })
    onlineIDs = ''
    for b in a:
        if(b['online']): onlineIDs += str(b['id']) + ','
    onlineIDs = onlineIDs[0:-1]
    hour = datetime.now().time().hour
    if (hour >= 10 and hour <= 21):
        send_msg(onlineIDs)
        print('sended!\n')
    sleep(600)