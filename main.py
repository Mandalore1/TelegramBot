from urllib.parse import urljoin

import telebot
import requests
from settings import TOKEN

DEFAULT_MESSAGE = """
/dog: получить случайное изображение собаки
/cat: получить случайное изображение кошки
/word [слово]: получить определение слова (только английский)
"""
DOG_PICTURES_URL = "https://dog.ceo/api/breeds/image/random"
CAT_PICTURES_URL = "https://cataas.com/cat?json=true"
WORD_DEFINITIONS_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, DEFAULT_MESSAGE)

    elif message.text == "/dog":
        send_dog_picture(message)

    elif message.text == "/cat":
        send_cat_picture(message)

    elif message.text.startswith("/word"):
        word = message.text[6:]
        if not word.isalpha():
            bot.send_message(message.from_user.id, "После /word должно идти слово для поиска!")
            return
        send_word_definition(message, word)

    else:
        bot.send_message(message.from_user.id, "Я тебя не понял. Напиши /help для просмотра списка доступных команд")


def send_dog_picture(message):
    response_json = requests.get(DOG_PICTURES_URL).json()
    bot.send_message(message.from_user.id, response_json["message"])


def send_cat_picture(message):
    response_json = requests.get(CAT_PICTURES_URL).json()
    bot.send_message(message.from_user.id, urljoin("https://cataas.com", response_json["url"]))


def send_word_definition(message, word):
    response = requests.get(urljoin(WORD_DEFINITIONS_URL, word))
    if response.status_code == 404:
        bot.send_message(message.from_user.id, f"Слово {word} не найдено в словаре")
        return

    response_json = response.json()
    bot_response_text = f"Слово {word}\n"
    for meaning in response_json[0]["meanings"]:
        part_of_speech = meaning["partOfSpeech"]
        definition = meaning["definitions"][0]["definition"]
        bot_response_text += f"{part_of_speech}: {definition}\n"

    bot.send_message(message.from_user.id, bot_response_text)


bot.polling(none_stop=True, interval=0)
