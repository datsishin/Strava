import glob
import logging
import time

from telebot.types import InputMediaPhoto
import telebot
import os
from dotenv import load_dotenv

from json_worker import generation_analyse
from main import get_mileage_for_service
from stats_graber import get_volume_stats, get_full_stats

load_dotenv()

token = os.getenv('TELEGRAM_API_TOKEN')

first_user_id = os.getenv('FIRST_USR_ID')
second_user_id = os.getenv('SECOND_USER_ID')

bot = telebot.TeleBot(token)

nl = '\n'


@bot.message_handler(commands=['start'])
def say_hi(message):
    text = 'Hi!'
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['get_last_training'])
def get_training_data(message):
    user_id = message.chat.id
    text = generation_analyse(user_id)
    bot.send_message(user_id, text=text)

    map_path = 'media/map.png'
    power_path = 'media/graph_by_power.png'
    hr_path = 'media/graph_by_hr.png'
    list_of_pic = []

    if os.path.exists(map_path):
        list_of_pic.append(InputMediaPhoto(open(map_path, 'rb')))
    if os.path.exists(power_path):
        list_of_pic.append(InputMediaPhoto(open(power_path, 'rb')))
    if os.path.exists(hr_path):
        list_of_pic.append(InputMediaPhoto(open(hr_path, 'rb')))

    bot.send_media_group(user_id, list_of_pic, disable_notification=True)

    files = glob.glob('media/*')
    for f in files:
        os.remove(f)


@bot.message_handler(commands=['time_statistics'])
def get_statistics(message):
    user_id = message.chat.id
    data = get_volume_stats(user_id)
    bot.send_message(user_id, text=f'Время тренировок за последние 7 дней:{nl}{data[0]}'
                                   f'{nl}'
                                   f'{nl}'
                                   f'Время тренировок за последние 30 дней:{nl}{data[1]}'
                                   f'{nl}'
                                   f'{nl}'
                                   f'Время тренировок за последние 365 дней:{nl}{data[2]}'
                                   f'{nl}'
                                   f'{nl}'
                                   f'Время тренировок за все время:{nl}{data[3]}')


@bot.message_handler(commands=['service'])
def get_service_info(message):
    user_id = message.chat.id
    text = get_mileage_for_service()
    bot.send_message(user_id, text=text)


@bot.message_handler(commands=['get_full_statistics'])
def get_fully_stat(message):
    user_id = message.chat.id
    text = get_full_stats(user_id)
    bot.send_message(user_id, text=text)


while True:
    try:
        logging.info("Bot running")
        bot.polling(none_stop=True, timeout=10)
        break
    except telebot.apihelper.ApiException as ex:
        logging.error(ex)
        bot.stop_polling()

        time.sleep(3)

        logging.info("Running again!")
