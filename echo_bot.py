import telebot

from config import TG_TOKEN
import requests
import json

bot = telebot.TeleBot(TG_TOKEN)  # Insert your Telegram API Token here


@bot.message_handler(commands=['start'])  # Command "/start" (First command)
def send_welcome(message):
    bot.reply_to(message, "Use /help to get list of commands")  # Bot is replying you


@bot.message_handler(commands=['help'])  # Command "/help"
def send_welcome(message):
    bot.reply_to(message,
                 "/weather - Command to find out the weather in the city , /help - List of all commands")  # Bot is giving you list of all commands


@bot.message_handler(commands=['weather'])  # Command "/weather"
def send_weather(message):
    r = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q={}&appid=ff22fb82984d3a2972c49c259b53f6f6'.format(
            message.text[8:]))  # Sending API request to "openweathermap.org"
    with open('weather.json', 'w') as f:
        f.write(r.text)  # Creating file with reply from "openweathermap.org"

    with open('weather.json') as f:
        text = json.load(f)  # Getting JSON text

    if message.text[8:] is None or message.text[8:] == '':  # If user send "/weather" without city
        bot.reply_to(message, 'Enter /weather <City name> to find out the weather!')
    elif text['cod'] == 200:  # If city in the command is found:
        bot.reply_to(message,
                     'In {} {} degrees'.format(message.text[8:], round(text['main']['feels_like'] - 274.15)))
    else:  # If city in the command is not found:
        bot.reply_to(message, 'City not found!'.format(message.text[8:]))


bot.polling(none_stop=True, interval=0)  # Start bot
