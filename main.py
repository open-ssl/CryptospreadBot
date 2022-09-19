""" Основной модуль """

from telebot import types

from bot_config import bot
from handlers import HANDLER_MAP
from helpers.constants import BotMessage


@bot.message_handler(content_types=['text'])
def handle_user_massage(message: types.Message) -> None:
    """
    Основной обработчик сообщений от пользователя
    """
    handler = HANDLER_MAP.get(message.text)
    if handler is not None:
        handler(message)
        return

    bot.send_message(message.chat.id, BotMessage.UNKNOWN_ACTION_MESSAGE)


if __name__ == '__main__':
    bot.polling(none_stop=True)
