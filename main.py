import telebot
from telebot import types
from random import choice
from string import ascii_uppercase
from functools import partial
from helpers.helpers import add_admin_config

from helpers import helpers
from helpers.helpers import (
    Const,
    BotActualCommands,
    post_request,
    log_error_in_file,
)

from helpers.constants import BotMessage

bot = telebot.TeleBot(helpers.API_TOKEN)
SUPPORT_URL = 'https://t.me/CryptospreadNetSupport'
CRYPTOSPREAD_MAIN = 'https://lk.cryptospread.net'


@bot.message_handler(commands=['start'])
def start_command(message):
    """
    Показываем главное меню бота
    :return: Отображаем кнопки Получить пробный, Купить подписку или Написать в поддержку
    Если это админ, то ему даем еще и кнопку админки
    """
    user_first_name = message.chat.first_name
    keyboard = types.InlineKeyboardMarkup()
    bot_actual_commands = BotActualCommands.get_main_menu_commands()
    for callback_command, command_text in bot_actual_commands.items():
        keyboard_button = partial(types.InlineKeyboardButton, text=command_text,
                                  callback_data=callback_command, url=None)
        if callback_command == BotActualCommands.WRITE_DEVELOPERS_COMMAND:
            keyboard.add(keyboard_button(url=SUPPORT_URL))
            continue
        keyboard.add(keyboard_button())

    add_admin_config(message, keyboard)

    bot.send_message(message.chat.id, BotMessage.START_BOT_MESSAGE.format(user_first_name), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    Проверяем все колбеки и в зависимости от выбранной секции, основная или админская, даем ему ответ на сообщение
    """
    if call.message:
        if call.data == BotActualCommands.MAIN_MENU:
            start_command(call.message)
        elif call.data in BotActualCommands.get_all_commands():
            if call.data == BotActualCommands.GET_ACCESS_KEY_COMMAND:
                bot.send_message(call.message.chat.id, BotMessage.CHECK_USER_FOR_CODE_MESSAGE)
                create_code_for_user(call.message)
            elif call.data == BotActualCommands.BUY_ACCESS_COMMAND:
                create_menu_for_pay_info(call.message)
            elif call.data == BotActualCommands.WRITE_DEVELOPERS_COMMAND:
                bot.send_message(call.message.chat.id, BotMessage.WRITE_DEVELOPERS_MESSAGE)
            elif call.data == BotActualCommands.USER_PAID_ACCESS:
                message = bot.send_message(call.message.chat.id, BotMessage.AFTER_USER_PAID_ACCESS)
                # bot.register_next_step_handler(message, user_inputed_data)
        elif call.data in BotActualCommands.get_all_admin_commands():
            if call.data == BotActualCommands.ADMIN_SECTION:
                create_admin_panel(call.message)
            elif call.data == BotActualCommands.ADD_ACCESS_FOR_USER:
                create_menu_for_adding_user(call.message)
            elif call.data == BotActualCommands.ANSWER_FOR_USER:
                bot.send_message(call.message.chat.id, BotMessage.ANSWER_FOR_USER_GREETING)
            elif call.data == BotActualCommands.ADD_ACCESS_WITH_TELEGRAM:
                message = bot.send_message(call.message.chat.id, BotMessage.INPUT_TELEGRAM_USER_FOR_ACCESS)
                bot.register_next_step_handler(message, create_access_for_user_by_admin, (Const.TELEGRAM, ))
            elif call.data == BotActualCommands.ADD_ACCESS_WITH_EMAIL:
                message = bot.send_message(call.message.chat.id, BotMessage.INPUT_EMAIL_USER_FOR_ACCESS)
                bot.register_next_step_handler(message, create_access_for_user_by_admin, (Const.EMAIL, ))


def create_code_for_user(message):
    """
    Генерим 16-значный код для юзера
    Делаем запрос на сервис, который проверяет
    1. Есть ли такой юзер у нас в базе вообще
    2. Не генеририровали ли мы для пользователя код ранее
    Если запрос вернул валидный результат, то показываем пользователю код, иначе ошибка с сервиса
    """
    try:
        username = message.chat.username
        user_id = message.chat.id
        new_generated_code = ''.join(choice(ascii_uppercase) for _ in range(helpers.GENERATED_CODE_LENGTH))
        json_data = {
            Const.GENERATED_CODE: new_generated_code,
            Const.TELEGRAM_USER: username,
            Const.TELEGRAM_ID: user_id
        }
        request_result = post_request(helpers.CREATE_NEW_CODE_END_POINT, json_data=json_data)
        request_result = request_result.json()

        result_msg = BotMessage.SUCCESS_GENERATED_CODE_MESSAGE.format(new_generated_code)
        if not request_result.get(Const.ORERATION_RESULT):
            result_msg = request_result.get(Const.ERROR_MESSAGE)
        bot.send_message(message.chat.id, result_msg)

        keyboard = types.InlineKeyboardMarkup()
        keyboard_commands = BotActualCommands.get_generate_code_menu()
        for callback_command, command_text in keyboard_commands.items():
            if callback_command == BotActualCommands.GO_TO_CRYPTOSPREAD:
                keyboard.add(types.InlineKeyboardButton(text=command_text, callback_data=callback_command, url=CRYPTOSPREAD_MAIN))
                continue
            keyboard.add(types.InlineKeyboardButton(text=command_text, callback_data=callback_command))
        bot.send_message(message.chat.id, BotMessage.NEXT_SECTION_GREETING, reply_markup=keyboard)
    except:
        log_error_in_file()
        bot.send_message(message.chat.id, BotMessage.ERROR_MESSAGE)


def create_access_for_user_by_admin(message, extra_args):
    """
    Админ нажал кнопку добавление юзера через телеграм или почту
    :param message: обьект сессии сообщения после нажатия
    :param extra_args: tuple: Обьект дополнительной информации
    """
    try:
        # Тип того, через что админ пытается добавить пользователя
        access_type = extra_args[0]

        inputed_data = message.html_text.strip()
        sub_type, access_value = inputed_data.split()

        json_data = {
            Const.ADMIN_ID: message.chat.id,
            Const.ADMIN_USERNAME: message.chat.username,
            Const.ACCESS_TYPE: access_type,
            Const.ACCESS_VALUE: access_value,
            Const.SUB_TYPE: int(sub_type)
        }

        request_result = post_request(helpers.CREATE_NEW_ACCESS_END_POINT, json_data=json_data).json()
        result_msg = BotMessage.SUCCESS_ACCESS_FOR_USER.format(access_type, access_value, sub_type)
        if not request_result.get(Const.ORERATION_RESULT):
            result_msg = request_result.get(Const.ERROR_MESSAGE)
        """
        # todo
        #  Вот здесь если успех надо отправить пользователю сообщение о том, что подписка для него оформлена.
        #  для этого надо выкинуть с бека его телеграм айди
        # todo update:
        # айдишник вроде выкинул, но надо потестировать
        telegram_id = request_result.get(Const.TELEGRAM_ID)
        user_id = request_result.get(Const.USER_ID)
        """
        bot.send_message(message.chat.id, result_msg)

    except Exception as e:
        log_error_in_file()
        bot.send_message(message.chat.id, BotMessage.ERROR_MESSAGE)


@bot.message_handler(content_types=['text'])
def start(message):
    """
    Чекаем все сообщения от пользователя
    """
    if message.text != '/start':
        bot.send_message(message.from_user.id, BotMessage.UNKNOWN_ACTION_MESSAGE)


def create_admin_panel(message):
    """
    Кликнули по кнопке Админка
    :return: Выдаем меню выбора Добавить пользователя или Ответить в поддержку
    """
    keyboard = types.InlineKeyboardMarkup()
    bot_actual_commands = BotActualCommands.get_admin_commands_level2()
    for callback_command, command_text in bot_actual_commands.items():
        keyboard.add(types.InlineKeyboardButton(text=command_text, callback_data=callback_command))

    bot.send_message(message.chat.id, BotMessage.NEXT_SECTION_GREETING, reply_markup=keyboard)


def create_menu_for_adding_user(message):
    """
    Нажали на Добавить подписку для пользователя
    return: Выдаем меню выбора через что добавляем - Телега или Почта
    """
    keyboard = types.InlineKeyboardMarkup()
    bot_actual_commands = BotActualCommands.get_admin_commands_level3()
    for callback_command, command_text in bot_actual_commands.items():
        keyboard.add(types.InlineKeyboardButton(text=command_text, callback_data=callback_command))

    bot.send_message(message.chat.id, BotMessage.ADD_ACCESS_FOR_USER_GREETING, reply_markup=keyboard)


def create_menu_for_pay_info(message):
    keyboard = types.InlineKeyboardMarkup()
    bot_actual_commands = BotActualCommands.get_commands_for_pay()
    for callback_command, command_text in bot_actual_commands.items():
        keyboard_button = partial(types.InlineKeyboardButton, text=command_text, callback_data=callback_command, url=None)
        if callback_command == BotActualCommands.USER_PAID_ACCESS:
            keyboard.add(keyboard_button(url=SUPPORT_URL))
            continue
        keyboard.add(keyboard_button())

    bot.send_message(message.chat.id, BotMessage.BUY_ACCESS_MESSAGE, reply_markup=keyboard)


# def user_inputed_data(message):
#     bot.send_message(message.chat.id, 'Спасибо, что что-то ввели')


if __name__ == '__main__':
    bot.polling(none_stop=True)
