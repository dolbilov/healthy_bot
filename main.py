'''
Healthy Bot
v 0.2.1-rc
(c) Dolbilov Kirill 2020
'''

from Bot import *
from config import *

vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, group_id=groupID)

b = Bot()

# ------------   MAIN PART   -----------
print('Bot started')
while (True):
    b.handle_new_messages()
    intervals += 1
    if intervals == MAX_INTERVALS:
        intervals = 0
        onlineIDs = b.get_online_str()
        time = datetime.now().time()
        hour = time.hour + difference_UTC
        min = time.minute
        sec = time.second
        try:
            if (hour == 10) and (min < 10):
                b.send_msg(choice(b.phrases_gm), onlineIDs, photo=start + choice(b.pics))
                print_time(hour, min, sec)
            elif (hour == 23) and (time.minute < 10):
                b.send_msg(choice(b.phrases_gn) + ' ' + choice(smiles_gn), onlineIDs, photo=start + choice(b.pics_gn))
                print_time(hour, min, sec)
            elif (hour >= 10 and hour <= 22):
                b.send_msg(choice(b.phrases) + ' ' + choice(smiles), onlineIDs, photo=start + choice(b.pics))
                print_time(hour, min, sec)
        except Exception as e:
            print(e)
            print(onlineIDs)

    sleep(sleepTime)
