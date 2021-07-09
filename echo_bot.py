import telebot

from config import TG_TOKEN
import requests
import json


temp = 'K'  # Default temperature unit (Kelvin)
bot = telebot.TeleBot(TG_TOKEN)  # Insert your Telegram API Token here


@bot.message_handler(commands=['start'])  # Command "/start" (First command)
def send_welcome(message):
    bot.reply_to(message, "Use /help to get list of commands")  # Bot is replying you


@bot.message_handler(commands=['help'])  # Command "/help"
def send_welcome(message):
    bot.reply_to(message,
                 "/weather - Command to find out the weather in the city, /help - List of all commands, /unit - Set unit (Kelvin, Celsius, Fahrenheit)")  # Bot is giving you list of all commands


@bot.message_handler(commands=['unit'])  # Command "/unit"
def changer_temp_unit(message):
    unit = message.text[6:]  # Unit
    if unit == ' ' or unit == '':  # If user enter "/unit "
        bot.reply_to(message, "To change your temperature unit you should enter \"/unit <unit(K - Kelvin, F - Fahrenheit, C - Celsius)>\"")
    else:  # If user enter unit to "/unit"
        global temp
        temp = message.text[6:].upper()
        if temp == 'K' or temp == 'C' or temp == 'F':  # If unit is correct
            bot.reply_to(message, 'Temperature unit is {} now!'.format(temp))
        else:  # If unit is not correct
            temp = 'K'  # Default unit
            bot.reply_to(message, '{} is not found! Unit is "Kelvin" now'.format(message.text[temp:]))

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
        if temp == 'C':  # If unit is Celsius
            bot.reply_to(message,
                         'It\'s {} degrees Celsius in {}'.format(round(text['main']['feels_like'] - 274.15),
                                                                 message.text[8:]))
        elif temp == 'K':  # If unit is Kelvin
            bot.reply_to(message,
                         'It\'s {} degrees Kelvin in {}'.format(round(text['main']['feels_like']),
                                                                 message.text[8:]))
        else:  # If unit is Fahrenheit
            bot.reply_to(message,
                         'It\'s {} degrees Fahrenheit in {}'.format(round(1.8*(text['main']['feels_like']-273)+32),
                                                                 message.text[8:]))
    else:  # If city in the command is not found:
        bot.reply_to(message, 'City not found!'.format(message.text[8:]))


bot.polling(none_stop=True, interval=0)  # Starting bot
