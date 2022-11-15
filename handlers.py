""" Модуль с функциями-обработчиками сообщений от пользователя """

from functools import partial
from random import choice
from string import ascii_uppercase

from telebot import types

from bot_config import bot
from helpers import helpers
from helpers.constants import BotMessage, Const, UserMessage


@bot.message_handler(commands=['start'])
def start_command(message: types.Message) -> None:
    """
    Показываем главное меню бота
    Отображаем кнопки Получить пробный, Купить подписку или Написать в поддержку
    Если это админ, то ему даем еще и кнопку админки
    """
    user_first_name = message.chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for command_text in UserMessage.get_main_menu_commands():
        keyboard.add(types.KeyboardButton(text=command_text))

    add_admin_config(message, keyboard)

    bot.send_message(message.chat.id, BotMessage.START_BOT_MESSAGE.format(user_first_name), reply_markup=keyboard)


def custom_send_message(message: types.Message, text: str) -> None:
    """
    Обертка над методом апи send_message для отправки кастомного сообщения
    """
    bot.send_message(message.chat.id, text)


def create_code_for_user(message: types.Message) -> None:
    """
    Генерим 16-значный код для юзера
    Делаем запрос на сервис, который проверяет
    1. Есть ли такой юзер у нас в базе вообще
    2. Не генеририровали ли мы для пользователя код ранее
    Если запрос вернул валидный результат, то показываем пользователю код, иначе ошибка с сервиса
    """
    bot.send_message(message.chat.id, BotMessage.CHECK_USER_FOR_CODE_MESSAGE)

    try:
        username = message.chat.username
        user_id = message.chat.id
        new_generated_code = ''.join(choice(ascii_uppercase) for _ in range(helpers.GENERATED_CODE_LENGTH))
        json_data = {
            Const.GENERATED_CODE: new_generated_code,
            Const.TELEGRAM_USER: username,
            Const.TELEGRAM_ID: user_id
        }
        request_result = helpers.post_request(helpers.CREATE_NEW_CODE_END_POINT, json_data=json_data)
        request_result = request_result.json()

        result_msg = BotMessage.SUCCESS_GENERATED_CODE_MESSAGE.format(new_generated_code)
        if not request_result.get(Const.ORERATION_RESULT):
            result_msg = request_result.get(Const.ERROR_MESSAGE)
        bot.send_message(message.chat.id, result_msg)
    except Exception:
        helpers.log_error_in_file()
        bot.send_message(message.chat.id, BotMessage.ERROR_MESSAGE)


def create_menu_for_pay_info(message: types.Message) -> None:
    """
    Кликнули по кнопке Купить подписку
    Выдаем меню выбора Оплачено и В главное меню
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for command_text in UserMessage.get_commands_for_pay():
        keyboard.add(types.KeyboardButton(text=command_text))

    bot.send_message(message.chat.id, BotMessage.BUY_ACCESS_MESSAGE, reply_markup=keyboard)


@helpers.admin_action
def ensure_payment(message: types.Message) -> None:
    """
    Убедимся, что пользователь заплатил
    """
    # TODO
    bot.send_message(message.chat.id, BotMessage.SAMPLE_TEXT)


@helpers.admin_action
def create_admin_panel(message: types.Message) -> None:
    """
    Кликнули по кнопке Админка
    Выдаем меню выбора Добавить пользователя или Ответить в поддержку
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for command_text in UserMessage.get_main_admin_commands():
        keyboard.add(types.KeyboardButton(text=command_text))

    bot.send_message(message.chat.id, BotMessage.NEXT_SECTION_GREETING, reply_markup=keyboard)


@helpers.admin_action
def create_menu_for_adding_user(message: types.Message) -> None:
    """
    Нажали на Добавить подписку для пользователя
    return: Выдаем меню выбора через что добавляем - Телега или Почта
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for command_text in UserMessage.get_admin_commands_for_adding_user():
        keyboard.add(types.InlineKeyboardButton(text=command_text))

    bot.send_message(message.chat.id, BotMessage.ADD_ACCESS_FOR_USER_GREETING, reply_markup=keyboard)


@helpers.admin_action
def create_access_for_user_by_admin(message: types.Message, extra_args: tuple) -> None:
    """
    Админ нажал кнопку добавление юзера через телеграм или почту
    :param message: обьект сессии сообщения после нажатия
    :param extra_args: tuple: Обьект дополнительной информации
    """
    access_type = extra_args[0]
    if access_type == Const.TELEGRAM:
        bot.send_message(message.chat.id, BotMessage.INPUT_TELEGRAM_USER_FOR_ACCESS)
    else:
        bot.send_message(message.chat.id, BotMessage.INPUT_EMAIL_USER_FOR_ACCESS)

    try:
        # Тип того, через что админ пытается добавить пользователя
        inputed_data = message.html_text.strip()
        sub_type, access_value = inputed_data.split()

        json_data = {
            Const.ADMIN_ID: message.chat.id,
            Const.ADMIN_USERNAME: message.chat.username,
            Const.ACCESS_TYPE: access_type,
            Const.ACCESS_VALUE: access_value,
            Const.SUB_TYPE: int(sub_type)
        }

        request_result = helpers.post_request(helpers.CREATE_NEW_ACCESS_END_POINT, json_data=json_data).json()
        result_msg = BotMessage.SUCCESS_ACCESS_FOR_USER.format(access_type, access_value, sub_type)
        if not request_result.get(Const.ORERATION_RESULT):
            result_msg = request_result.get(Const.ERROR_MESSAGE)
        # todo
        #  Вот здесь если успех надо отправить пользователю сообщение о том, что подписка для него оформлена.
        #  для этого надо выкинуть с бека его телеграм айди
        # todo update:
        # айдишник вроде выкинул, но надо потестировать
        telegram_id = result_msg.get(Const.TELEGRAM_ID)
        bot.send_message(message.chat.id, result_msg)

    except Exception:
        helpers.log_error_in_file()
        bot.send_message(message.chat.id, BotMessage.ERROR_MESSAGE)


# @helpers.admin_action
# def add_admin_config(message: types.Message, keyboard: types.ReplyKeyboardMarkup) -> None:
#     """
#     Добавляет кнопку Админка (при необходимости)
#     """
#     keyboard.add(types.KeyboardButton(text=UserMessage.ADMIN_NAME))


HANDLER_MAP = {
    UserMessage.MAIN_MENU: start_command,
    UserMessage.GET_TRIAL_KEY: create_code_for_user,
    UserMessage.BUY_ACCESS: create_menu_for_pay_info,
    UserMessage.WRITE_US: partial(custom_send_message, text=BotMessage.WRITE_DEVELOPERS_MESSAGE),
    UserMessage.USER_PAID_ACCESS: ensure_payment,
    # UserMessage.ADMIN_NAME: create_admin_panel,
    UserMessage.ADD_SUB: create_menu_for_adding_user,
    # UserMessage.ANSWER_FOR_USERS: partial(custom_send_message, text=BotMessage.ANSWER_FOR_USER_GREETING),
    UserMessage.ADD_WITH_TELEGRAM: partial(create_access_for_user_by_admin, extra_args=(Const.TELEGRAM, )),
    UserMessage.ADD_WITH_EMAIL: partial(create_access_for_user_by_admin, extra_args=(Const.EMAIL, )),
    UserMessage.CANCEL: create_admin_panel,
}
