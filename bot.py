import os
import requests
import telebot
import urllib
import json
import pprint
import jsonpickle
import datetime
from pprint import pprint
import time, calendar
from datetime import date
from telebot import types

with open("token.txt") as f:
    TOKEN = f.read()
    print(TOKEN)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Привіт, {0.first_name}!\nЯ - <b>бот {1.first_name}</b>!\n"
                                      "Мене написав Олександр як міні-пет-проект, щоб попрактикуватись.\n"
                                      "Назву населеного пункту вводити на англійській.".format(message.from_user, bot.get_me()),
                     parse_mode='html')

@bot.message_handler(commands=['photo'])
def photo(message):
    with urllib.request.urlopen("https://api.thecatapi.com/v1/images/search") as url:
        data = json.loads(url.read().decode())
        photoAddr = data[0]['url']
        print(photoAddr)
        bot.send_photo(message.chat.id, photoAddr)


@bot.message_handler(commands=['weather'])
def weather_forecast(message):
    msg = bot.send_message(message.chat.id, "Введіть назву населеного пункта")
    bot.register_next_step_handler(msg, get_weather)


def get_weather(message):
    print(message.text)
    try:
        date_today = str(datetime.datetime.today()).split(" ", 1)[0]
        r = requests.get(
            #& appid = {open_weather_token}
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid=dbd760e3f9cbe5f7ab5f8fb98bef14ab&units=metric"
        )
        data = r.json()
        city = data["name"]
        temp = data["main"]["temp"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        description = data["weather"][0]["description"]
        wind = data["wind"]["speed"]
        humidity = data["main"]["humidity"]  # вологість
        pressure = data["main"]["pressure"]
        sunrise_timestamp = str(datetime.datetime.fromtimestamp(data["sys"]["sunrise"])).split()[-1]
        sunset_timestamp = str(datetime.datetime.fromtimestamp(data["sys"]["sunset"])).split()[-1]
        bot.send_message(message.chat.id, f"Погодка на {date_today} у населеному пункті {city}:\n"
              f"Температура повітря: {temp}°C,\n"
              f"Схід сонця о {sunrise_timestamp}, захід почнеться о {sunset_timestamp}\n"
              #f"Мінімальна T: {temp_min}, Максимальна T: {temp_max},\n"
              f"Короткий опис погоди: {description},\n"
              f"Швидкість вітру {wind}м/с,\n"
              f"Вологість: {humidity}, Тиск {pressure}мм")
    except Exception as ex:
        bot.send_message(message.chat.id, ex)
        bot.send_message(message.chat.id, "Перевір назву нп!")


@bot.message_handler(commands=['get_my_id'])
def get_my_id(message):
    aidi = json.loads(jsonpickle.encode(message))
    user_id = "ID Твого телеграм акаунту: " + str(aidi['from_user']['id'])
    print(type(aidi))
    bot.send_message(message.chat.id, user_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
