import vk_api
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import choice
from config import *


def make_list(fileName):
    f = open('res/' + fileName, encoding='utf-8')
    arr = [str for str in f.readlines()]
    f.close()
    for i in range(len(arr)):
        arr[i] = arr[i].replace('\n', '')
    return arr


def print_time(hour, min, sec):
    min = str(min) if min >= 10 else '0' + str(min)
    sec = str(sec) if sec >= 10 else '0' + str(sec)
    print('gm dog sended at ', end='')
    print('{}:{}:{}'.format(hour, min, sec))


class Bot:
    """
    Initialization of bot.
    Initialization:
    1) keyboardStart - starting keyboard for users who deactivated bot.
    2) keyBoardActive - for users, who are active
    3) vk session
    4) all lists of users, pics etc
    """

    def __init__(self):
        self.keyboardStart = VkKeyboard(one_time=True)
        self.keyboardStart.add_button('Включить', color=VkKeyboardColor.POSITIVE)
        self.keyboardStart = self.keyboardStart.get_keyboard()

        self.keyboardActive = VkKeyboard(one_time=True)
        self.keyboardActive.add_button('Можно еще фото собачки?', color=VkKeyboardColor.POSITIVE)
        self.keyboardActive.add_button('Отключить', color=VkKeyboardColor.NEGATIVE)
        self.keyboardActive = self.keyboardActive.get_keyboard()

        self.vk_session = vk_api.VkApi(token=token)

        self.ids = make_list('users.txt')
        self.pics = make_list('pics.txt')
        self.pics_gn = make_list('pics_gn.txt')
        self.phrases = make_list('phrases.txt')
        self.phrases_gm = make_list('phrases_gm.txt')
        self.phrases_gn = make_list('phrases_gn.txt')

    """
    @:param msg - message body
    @:param onlineIDs - guys which are active and online
    @:param photo - url to a dog to send
    @:param deactivating - param to check if we deactive. If deactive, use another keyboard
    """

    def send_msg(self, msg, onlineIDs, photo, deactivating=False):
        currentKeyboard = self.keyboardActive
        if deactivating:
            currentKeyboard = self.keyboardStart
        if photo == None:
            self.vk_session.method('messages.send', {'message': msg,
                                                     'random_id': get_random_id(),
                                                     'user_ids': onlineIDs,
                                                     'keyboard': currentKeyboard
                                                     })
        else:
            self.vk_session.method('messages.send', {'message': msg,
                                                     'random_id': get_random_id(),
                                                     'user_ids': onlineIDs,
                                                     'attachment': photo,
                                                     'keyboard': currentKeyboard
                                                     })

    """
    Previous name: check_new_messages. I\'ve changes name due to
    this function just handles new messages and responses them
    That is why now ot is handle_new_messages
    """
    def handle_new_messages(self):
        changed = False
        conversations = self.vk_session.method('messages.getConversations', {'count': 200,
                                                                             'filter': 'unread'
                                                                             })
        if (conversations['count'] == 0): return None
        for conv in conversations['items']:
            subject_id = str(conv['conversation']['peer']['id'])
            txt = conv['last_message']['text'].lower()
            if 'сяп' in txt or 'пасиб' in txt:
                self.send_msg(choice(['Всегда пожалуйста!', 'Рад стараться!', 'Вам спасибо!']), subject_id, None)
            if txt == 'начать':
                if subject_id in self.ids:
                    self.send_msg('Вы уже подписаны на рассылку', subject_id, None)
                else:
                    self.ids.append(subject_id)
                    self.send_msg('Вы успешно подписались на рассылку. В течение 10 минут бот скинет вам шабачку :)',
                                  subject_id,
                                  None)
                    changed = True
            if txt == 'включить':
                if subject_id in self.ids:
                    self.send_msg('Вы уже подписаны на рассылку', subject_id, None)
                else:
                    self.ids.append(subject_id)
                    self.send_msg('Вы подписались на рассылку', subject_id, None)
                    changed = True
            if txt == 'отключить':
                if subject_id in self.ids:
                    self.send_msg(
                        'Вы отписались от рассылки. Спасибо, что пользовались ботом. Если вам что-то не понравилось, пожалуйста, расскажите об этом [healthy_b0t|здесь]',
                        subject_id, None, True)
                    self.ids.remove(subject_id)
                    changed = True
                else:
                    self.send_msg('Вы не подписаны на рассылку :(', subject_id, None)
            if (changed):
                f = open('users.txt', 'w')
                for u in self.ids:
                    f.write(u + '\n')
                f.close()


    """
    creates a list of users to send them dog.
    """

    def get_online(self):
        ans = self.vk_session.method('users.get', {
            'user_ids': ','.join(self.ids),
            'fields': 'online'
        })
        onlineIDs = []
        for person in ans:
            if (person['online']):
                onlineIDs.append(person['id'])
        if len(onlineIDs) == 1:
            return str(onlineIDs[0])
        else:
            return onlineIDs


    """
    Previous name: getOnline
    returns string representaion of list of online users to send query to VK
    """
    def get_online_str(self):
        return ','.join(list(map(str, self.get_online())))
