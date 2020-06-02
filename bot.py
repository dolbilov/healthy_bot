'''
Healthy Bot
v 0.1.0-b
(c) Dolbilov Kirill 2020
'''

import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from time import sleep
from random import randint
from datetime import datetime
from config import *


vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, group_id=groupID)
vk = vk_session.get_api()

message = 'Выпрями спину! <3'
gn_message = 'Пора спать. Спокойной ночи. 😴'
att = 'photo-64987665_'

dogs_num = 457239133
dogs_count = 52
gn_dogs_num = 457239186
gn_dogs_count = 14
sleepTime = 10
dt = 3 # 0 for MSK 
MAX_INTERVALS = 60
intervals = MAX_INTERVALS - 1

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Включить', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Отключить', color=VkKeyboardColor.NEGATIVE)
keyboard = keyboard.get_keyboard()

try:
    f = open('users.txt')
except:
    print("File doesn't exist. Make file users.txt in the same directory with config.py and bot.py")
    quit()


ids = [str for str in f.readlines()]
f.close()
for i in range(len(ids)):
    ids[i] = ids[i].replace('\n', '')


def send_msg(msg, onlineIDs, photo):
    if photo == None:
        vk_session.method('messages.send', {'message': msg,
                                            'random_id': get_random_id(),
                                            'user_ids': onlineIDs,
                                            'keyboard' : keyboard
        })
    else:
        vk_session.method('messages.send', {'message': msg,
                                            'random_id': get_random_id(),
                                            'user_ids': onlineIDs,
                                            'attachment': photo,
                                            'keyboard': keyboard
                                            })

def check_new_messages():
    changed = False
    conversations = vk_session.method('messages.getConversations', {'count': 200,
                                                                    'filter': 'unread'
                                                                    })
    if (conversations['count'] == 0): return None
    for conv in conversations['items']:
        subject_id = str(conv['conversation']['peer']['id'])
        txt = conv['last_message']['text']
        if txt == 'Начать':
            ids.append(subject_id)
            send_msg('Вы успешно подписались на рассылку', subject_id, None)
            changed = True
        if txt == 'Включить':
            if subject_id in ids:
                send_msg('Вы уже подписаны на рассылку', subject_id, None)
            else:
                ids.append(subject_id)
                send_msg('Вы подписались на рассылку', subject_id, None)
                changed = True
        if txt == 'Отключить':
            if subject_id in ids:
                send_msg(
                    'Вы отписались от рассылки. Спасибо, что пользовались ботом. Если вам что-то не понравилось, пожалуйста, расскажите об этом [healthy_b0t|здесь]',
                    subject_id, None)
                ids.remove(subject_id)
                changed = True
            else:
                send_msg('Вы не подписаны на рассылку :(', subject_id, None)
        if (changed):
            f = open('users.txt', 'w')
            for u in ids:
                f.write(u + '\n')
            f.close()


print('Bot started')
while (True):
    check_new_messages()

    intervals += 1
    if intervals == MAX_INTERVALS:
        intervals = 0
        ans = vk_session.method('users.get', {'user_ids': ','.join(list(map(str, ids))),
                                        'fields': 'online'
        })


        onlineIDs = []
        for person in ans:
            if(person['online']):
                onlineIDs.append(person['id'])
        time = datetime.now().time()
        hour = time.hour + dt
        try:
            if (hour == 23) and (time.minute < 10):
                send_msg(gn_message, ','.join(list(map(str, onlineIDs))), att + str(gn_dogs_num + randint(0,gn_dogs_count)))
                print('gn dog sended at ', time)
            elif (hour >= 10 and hour <= 22):
                send_msg(message, ','.join(list(map(str, onlineIDs))), att + str(dogs_num + randint(0,dogs_count)))
                print('dog sended at ', time)
        except Exception as e:
            print(e)
            print(onlineIDs)

    sleep(sleepTime)
