""" Модуль с функциямим хелперами """

import sys
from time import sleep
from traceback import print_exception
from typing import Callable

from telebot import types
from requests_futures import sessions

from bot_config import bot
from helpers.constants import BotMessage, Creads


def log_error_in_file():
    error_file = 'error_log.txt'
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        with open(error_file, 'a') as file:
            print('_______________________________________', file=file)
            print_exception(exc_type, exc_value, exc_traceback, file=file)
            print('_______________________________________', file=file)
    except Exception as e:
        print(e)
    finally:
        print('end log error')


def get_session_for_request():
    return sessions.FuturesSession()


def post_request(url, json_data):
    session = get_session_for_request()

    while True:
        try:
            request_result = session.post(url, json=json_data)
            break
        except Exception as e:
            print('Unknown error %s' % e)
            sleep(0.5)

    return request_result.result()


def is_admin(message: types.Message) -> bool:
    """
    Возвращает  True, если пользователь - админ
    """
    unknown_username = message.chat.username
    unknown_user_id = message.chat.id
    admins = Creads.get_admins_creads()

    for admin_id, admin_username in admins.items():
        if unknown_user_id == admin_id and unknown_username == admin_username:
            return True

    return False


def admin_action(func: Callable) -> Callable:
    """
    Декоратор, скрывающий функционал админки для обычных пользователей
    Если пользователь не админ, напишем ему, что он ввел неизвестную команду
    """
    def wrapper(message: types.Message, *args, **kwargs) -> None:
        if is_admin(message):
            func(message, *args, **kwargs)
        else:
            bot.send_message(message.chat.id, BotMessage.UNKNOWN_ACTION_MESSAGE)

    return wrapper
