import requests
import configparser
import logging
from datetime import datetime
import os
import random

from Constants import GOOD_MORNING, DIMA_PHOTOS, SVETA_PHOTOS, MEMORIE_PHOTOS, TISHA_PHOTOS

config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(format='%(pathname)s  %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

token = config['DEFAULT']['token']
PATH = '/Users/savindmitriy/Desktop/TELEBOT/PHOTOS/'

GREETINGS = ('здравствуй', 'привет', 'ку', 'здорово')
SVETA = ('я', 'света', 'красавица')
DIMA = ('димка', 'дима', 'любимый')
TISHA = ('тиша', 'тишка')
MEMORIES = ('милота', 'воспоминания', 'прошлое', 'счастье')

now = datetime.now()


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=10):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']

        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_photo(self, chat_id, photo):
        params = {'chat_id': chat_id, 'photo': photo}
        method = 'sendPhoto'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            return 0
        return last_update


def greeting(bot: BotHandler, message: str, hour: int, day: int, last_chat_id: str, last_chat_name: str):
    if message.lower() in GREETINGS and 0 <= hour < 12:
        bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
        day += 1

    elif message.lower() in GREETINGS and 12 <= hour < 17:
        bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
        day += 1

    elif message.lower() in GREETINGS and 17 <= hour < 24:
        bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
        day += 1
    return day


def photos(bot: BotHandler, message: str, last_chat_id: str):
    if message.lower() in SVETA:
        # all_files_in_directory = os.listdir(PATH + 'DIMA')
        # photo = random.choice(all_files_in_directory)
        # photo = all_files_in_directory[1]
        # doc = open(PATH+'DIMA/'+photo, 'rb')
        # bot.send_photo(last_chat_id, doc)
        bot.send_message(last_chat_id, random.choice(SVETA_PHOTOS))


    if message.lower() in DIMA:
        bot.send_message(last_chat_id, random.choice(DIMA_PHOTOS))

    if message.lower() in TISHA:
        bot.send_message(last_chat_id, random.choice(TISHA_PHOTOS))

    if message.lower() in MEMORIES:
        bot.send_message(last_chat_id, random.choice(MEMORIE_PHOTOS))


def main():
    greet_bot = BotHandler(token)
    new_offset = None
    today = now.day

    while True:
        hour = now.hour
        second = now.second
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()
        if last_update == 0:
            continue

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message'].get('text', '')
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if today == now.day:
            today = greeting(greet_bot, last_chat_text, hour, today, last_chat_id, last_chat_name)

        if hour == 10 and second == 0:
            greet_bot.send_message(last_chat_id, GOOD_MORNING)

        photos(greet_bot, last_chat_text, last_chat_id)

        new_offset = last_update_id + 1


if __name__ == '__main__':
    main()


