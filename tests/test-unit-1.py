import unittest
from unittest.mock import MagicMock
import requests
from bot import bot, get_weather


class TestBot(unittest.TestCase):

    def test_help(self):
        message = MagicMock()
        message.from_user = {'first_name': 'John'}
        bot.get_me = MagicMock()
        bot.get_me.return_value.first_name = 'TestBot'
        bot.send_message = MagicMock()
        bot.message_handler(commands=['help'])(message)
        bot.send_message.assert_called_with(message.chat.id, "Привіт, John!\nЯ - <b>бот TestBot</b>!\n"
                                      "Мене написав Олександр як міні-пет-проект, щоб попрактикуватись.\n"
                                      "Назву населеного пункту вводити на англійській.", parse_mode='html')

    def test_weather(self):
        message = MagicMock()
        message.text = 'Kyiv'
        requests.get = MagicMock()
        requests.get.return_value.json.return_value = {
            'name': 'Kyiv',
            'main': {'temp': 10, 'temp_min': 8, 'temp_max': 12},
            'sys': {'sunrise': 1647008794, 'sunset': 1647050268},
            'weather': [{'description': 'Cloudy'}],
            'wind': {'speed': 3},
            'main': {'humidity': 75, 'pressure': 1007}
        }
        bot.send_message = MagicMock()
        get_weather(message)
        bot.send_message.assert_called_with(message.chat.id, f"Погодка на {datetime.datetime.today().strftime('%Y-%m-%d')} у населеному пункті Kyiv:\n"
              f"Температура повітря: 10°C,\n"
              f"Схід сонця о 06:33:14, захід почнеться о 17:31:08\n"
              #f"Мінімальна T: 8, Максимальна T: 12,\n"
              f"Короткий опис погоди: Cloudy,\n"
              f"Швидкість вітру 3м/с,\n"
              f"Вологість: 75, Тиск 1007мм")

if name == 'main':
    unittest.main()
