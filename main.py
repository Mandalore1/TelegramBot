from urllib.parse import urljoin

import telebot
import requests
from settings import TOKEN

DEFAULT_MESSAGE = """
/dog: получить случайное изображение собаки
/cat: получить случайное изображение кошки
"""
DOG_PICTURES_URL = "https://dog.ceo/api/breeds/image/random"
CAT_PICTURES_URL = "https://cataas.com/cat?json=true"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, DEFAULT_MESSAGE)
    elif message.text == "/dog":
        send_dog_picture(message)
    elif message.text == "/cat":
        send_cat_picture(message)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понял. Напиши /help для списка доступных команд")


def send_dog_picture(message):
    response_json = requests.get(DOG_PICTURES_URL).json()
    bot.send_message(message.from_user.id, response_json["message"])


def send_cat_picture(message):
    response_json = requests.get(CAT_PICTURES_URL).json()
    bot.send_message(message.from_user.id, urljoin("https://cataas.com", response_json["url"]))


bot.polling(none_stop=True, interval=0)

print("Бот запущен")
