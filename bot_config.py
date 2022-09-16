""" Модуль конфигурации бота """

import telebot


API_TOKEN = '5686307192:AAGWxHH_auacIqrN6gXK2F3cBKJnpFqdXyg'
GENERATED_CODE_LENGTH = 16
# CREATE_NEW_CODE_END_POINT = 'http://cryptospread.net/create_code_for_user'
CREATE_NEW_CODE_END_POINT = 'http://127.0.0.1:5002/create_code_for_user'
# CREATE_NEW_ACCESS_END_POINT = 'http://cryptospread.net/create_new_access'
CREATE_NEW_ACCESS_END_POINT = 'http://127.0.0.1:5002/create_new_access'

bot = telebot.TeleBot(API_TOKEN)
