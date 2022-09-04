import telebot
from telebot import types
from random import choice
from string import ascii_uppercase

from helpers import helpers
from helpers.helpers import Const, BotActualCommands, post_request

bot = telebot.TeleBot(helpers.API_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    user_first_name = message.chat.first_name
    keyboard = types.InlineKeyboardMarkup()
    bot_actual_commands = BotActualCommands.get_all_commands()
    for callback_command, command_text in bot_actual_commands.items():
        keyboard.add(types.InlineKeyboardButton(text=command_text, callback_data=callback_command))

    bot.send_message(message.chat.id, helpers.START_BOT_MESSAGE.format(user_first_name), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data in BotActualCommands.get_all_commands():
            if call.data == BotActualCommands.GET_ACCESS_KEY_COMMAND:
                bot.send_message(call.message.chat.id, helpers.CHECK_USER_FOR_CODE_MESSAGE)
                create_code_for_user(call.message)
            elif call.data == BotActualCommands.BUY_ACCESS_COMMAND:
                bot.send_message(call.message.chat.id, helpers.BUY_ACCESS_MESSAGE)
            elif call.data == BotActualCommands.WRITE_DEVELOPERS_COMMAND:
                bot.send_message(call.message.chat.id, helpers.WRITE_DEVELOPERS_MESSAGE)


def create_code_for_user(message):
    # генерируем код для юзера +
    # делаем запрос на проверку юзера в базе сайта
    # если статус запроса ок - отдаем код пользователю
    # если нет, показываем ошибку юзеру и прячем код

    username = message.chat.username
    new_generated_code = ''.join(choice(ascii_uppercase) for _ in range(helpers.GENERATED_CODE_LENGTH))
    json_data = {
        Const.GENERATED_CODE: new_generated_code,
        Const.TELEGRAM_USER: username
    }
    request_result = post_request(helpers.CREATE_NEW_CODE_END_POINT, json_data=json_data).json()

    result_msg = helpers.SUCCESS_GENERATED_CODE_MESSAGE.format(new_generated_code)
    if not request_result.get(Const.ORERATION_RESULT):
        result_msg = request_result.get(Const.EXTRA_DATA)
    bot.send_message(message.chat.id, result_msg)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text != '/start':
        bot.send_message(message.from_user.id, helpers.UNKNOWN_ACTION_MESSAGE)


if __name__ == '__main__':
    bot.polling(none_stop=True)
