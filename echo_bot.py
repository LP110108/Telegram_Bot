import telebot

from config import TG_TOKEN
import requests
import json

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi there, use /help to get list of commands")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,
                 "/weather - Command to find out the weather in the city , /help - List of all commands")


@bot.message_handler(commands=['weather'])
def send_weather(message):
    r = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q={}&appid=ff22fb82984d3a2972c49c259b53f6f6'.format(
            message.text[8:]))
    with open('weather.json', 'w') as f:
        f.write(r.text)

    with open('weather.json') as f:
        text = json.load(f)

    if message.text[8:] is None or message.text[8:] == '':
        bot.reply_to(message, 'Enter /weather <City name> to find out the weather!')
    elif text['cod'] == 200:
        bot.reply_to(message,
                     'In {} {} degrees'.format(message.text[8:], round(text['main']['feels_like'] - 274.15)))
    else:
        bot.reply_to(message, 'City not found!'.format(message.text[8:]))


bot.polling(none_stop=True, interval=0)
