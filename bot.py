'''
Healthy Bot
v 0.2.0-b
(c) Dolbilov Kirill 2020
'''

import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from time import sleep
from random import randint, choice
from datetime import datetime
from config import *


vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, group_id=groupID)
vk = vk_session.get_api()

smiles = ['❤', '💖', '💓', '💙', '💚', '💛', '💜', '🧡']
smiles_gn = ['🌜', '🌛', '🌃', '😴', '💤']

start = 'photo-64987665_'

period = 600
sleepTime = 10
dt = 3
MAX_INTERVALS = period // sleepTime
intervals = MAX_INTERVALS - 1


keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Включить', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Отключить', color=VkKeyboardColor.NEGATIVE)
keyboard = keyboard.get_keyboard()

def makeList(fileName):
    f = open('res/' + fileName, encoding='utf-8')
    arr = [str for str in f.readlines()]
    f.close()
    for i in range(len(arr)):
        arr[i] = arr[i].replace('\n', '')
    return arr

ids = makeList('users.txt')
pics = makeList('pics.txt')
pics_gn = makeList('pics_gn.txt')
phrases = makeList('phrases.txt')
phrases_gm = makeList('phrases_gm.txt')
phrases_gn = makeList('phrases_gn.txt')


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
        txt = conv['last_message']['text'].lower()
        if 'сяп' in txt  or 'пасиб' in txt:
            send_msg(choice(['Всегда пожалуйста!', 'Рад стараться!', 'Вам спасибо!']),subject_id, None)
        if txt == 'начать':
            if subject_id in ids:
                send_msg('Вы уже подписаны на рассылку', subject_id, None)
            else:
                ids.append(subject_id)
                send_msg('Вы успешно подписались на рассылку. В течение 10 минут бот скинет вам шабачку :)', subject_id, None)
                changed = True
        if txt == 'включить':
            if subject_id in ids:
                send_msg('Вы уже подписаны на рассылку', subject_id, None)
            else:
                ids.append(subject_id)
                send_msg('Вы подписались на рассылку', subject_id, None)
                changed = True
        if txt == 'отключить':
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

def getOnline():
    ans = vk_session.method('users.get', {
        'user_ids': ','.join(ids),
        'fields': 'online'
    })
    onlineIDs = []
    for person in ans:
        if (person['online']):
            onlineIDs.append(person['id'])
    if len(onlineIDs) == 1: return str(onlineIDs[0])
    else: return ','.join(list(map(str, onlineIDs)))

def printTime():
    time = datetime.now().time()
    min = time.minute
    min = str(min) if min >= 10 else '0' + str(min)
    sec = time.second
    sec = str(sec) if sec >= 10 else '0' + str(sec)
    print('{}:{}:{}'.format(hour,min,sec))



# ------------   MAIN PART   ------------
print('Bot started')
while (True):
    check_new_messages()

    intervals += 1
    if intervals == MAX_INTERVALS:
        intervals = 0
        onlineIDs = getOnline()
        time = datetime.now().time()
        hour = time.hour + dt
        min = time.minute
        try:
            if (hour == 10) and (min < 10):
                send_msg(choice(phrases_gm), onlineIDs, start + choice(pics))
                print('gm dog sended at ', end='')
                printTime()
            elif (hour == 23) and (time.minute < 10):
                send_msg(choice(phrases_gn) + ' ' + choice(smiles_gn), onlineIDs, start + choice(pics_gn))
                print('gn dog sended at ', end='')
                printTime()
            elif (hour >= 10 and hour <= 22):
                send_msg(choice(phrases) + ' ' + choice(smiles), onlineIDs, start + choice(pics))
                print('dog sended at ', end='')
                printTime()
        except Exception as e:
            print(e)
            print(onlineIDs)

    sleep(sleepTime)