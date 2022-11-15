import sys
from helpers.constants import BotMessage
from traceback import print_exception
from telebot import types
from time import sleep
from requests_futures import sessions


API_TOKEN = '5686307192:AAGWxHH_auacIqrN6gXK2F3cBKJnpFqdXyg'
GENERATED_CODE_LENGTH = 16
# закомментированное для дебага
CREATE_NEW_CODE_END_POINT = 'https://lk.cryptospread.net/create_code_for_user'
# CREATE_NEW_CODE_END_POINT = 'http://127.0.0.1:5000/create_code_for_user'
CREATE_NEW_ACCESS_END_POINT = 'https://lk.cryptospread.net/create_new_access'
# CREATE_NEW_ACCESS_END_POINT = 'http://127.0.0.1:5000/create_new_access'


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
            request_result = session.post(url, json=json_data, verify=False)
            break
        except Exception as e:
            print('Unknown error %s' % e)
            sleep(0.5)

    return request_result.result()


class BotActualCommands:
    GET_ACCESS_KEY_COMMAND = 'get_access_key'
    WRITE_DEVELOPERS_COMMAND = 'write_developers'
    BUY_ACCESS_COMMAND = 'buy_access'
    USER_PAID_ACCESS = 'user_paid_access'
    MAIN_MENU = 'main_menu'
    GO_TO_CRYPTOSPREAD = 'go_to_cryptospread'
    #######################################################
    # admin section
    ADMIN_SECTION = 'admin_section'
    ADD_ACCESS_FOR_USER = 'add_access_for_user'
    ANSWER_FOR_USER = 'answer_for_user'
    ADD_ACCESS_WITH_TELEGRAM = 'add_access_with_telegram'
    ADD_ACCESS_WITH_EMAIL = 'add_access_with_email'
    #######################################################

    @classmethod
    def get_main_menu_commands(cls):
        return {
            cls.GET_ACCESS_KEY_COMMAND: BotMessage.GET_TRIAL_KEY,
            cls.BUY_ACCESS_COMMAND: BotMessage.BUY_ACCESS,
            cls.WRITE_DEVELOPERS_COMMAND: BotMessage.WRITE_US,
        }

    @classmethod
    def get_all_commands(cls):
        return {
            cls.GET_ACCESS_KEY_COMMAND: BotMessage.GET_TRIAL_KEY,
            cls.BUY_ACCESS_COMMAND: BotMessage.BUY_ACCESS,
            cls.WRITE_DEVELOPERS_COMMAND: BotMessage.WRITE_US,
            cls.USER_PAID_ACCESS: BotMessage.USER_PAID_ACCESS,
            cls.MAIN_MENU: BotMessage.MAIN_MENU
        }

    @classmethod
    def get_commands_for_pay(cls):
        return {
            cls.USER_PAID_ACCESS: BotMessage.USER_PAID_ACCESS,
            cls.MAIN_MENU: BotMessage.MAIN_MENU
        }

    @classmethod
    def get_main_admin_commands(cls):
        return {
            cls.ADMIN_SECTION: BotMessage.ADMIN_NAME,
        }

    @classmethod
    def get_all_admin_commands(cls):
        return {
            cls.ADMIN_SECTION: BotMessage.ADMIN_NAME,
            cls.ADD_ACCESS_FOR_USER: BotMessage.ADD_SUB,
            # cls.ANSWER_FOR_USER: BotMessage.ANSWER_FOR_USERS,
            cls.ADD_ACCESS_WITH_TELEGRAM: BotMessage.ADD_WITH_TELEGRAM,
            cls.ADD_ACCESS_WITH_EMAIL: BotMessage.ADD_WITH_EMAIL
        }

    @classmethod
    def get_admin_commands_level2(cls):
        return {
            cls.ADD_ACCESS_FOR_USER: BotMessage.ADD_SUB,
            # cls.ANSWER_FOR_USER: BotMessage.ANSWER_FOR_USERS,
        }

    @classmethod
    def get_generate_code_menu(cls):
        return {
            cls.MAIN_MENU: BotMessage.MAIN_MENU,
            cls.GO_TO_CRYPTOSPREAD: BotMessage.GO_TO_CRYPTOSPREAD
            # cls.ANSWER_FOR_USER: BotMessage.ANSWER_FOR_USERS,
        }

    @classmethod
    def get_admin_commands_level3(cls):
        return {
            cls.ADD_ACCESS_WITH_TELEGRAM: BotMessage.ADD_WITH_TELEGRAM,
            cls.ADD_ACCESS_WITH_EMAIL: BotMessage.ADD_WITH_EMAIL,
        }


class Const:
    GENERATED_CODE = 'generatedCode'
    TELEGRAM_USER = 'telegramUser'
    TELEGRAM_ID = 'telegramId'
    EMAIL = 'email'
    TELEGRAM = 'telegram'

    ORERATION_RESULT = 'operationResult'
    ERROR_MESSAGE = 'errorMessage'
    SUCCESS_MESSAGE = 'successMessage'
    ACCESS_TYPE = 'accessType'
    ADMIN_USERNAME = 'adminUsername'
    ADMIN_ID = 'adminId'
    ACCESS_VALUE = 'accessValue'
    SUB_TYPE = 'subType'


class Creads:
    STAS_ID = 465146483
    STAS_USERNAME = 'Stanislav_Lukyanov'
    SLAVA_ID = 136756107
    SLAVA_USERNAME = 'VyacheslavBabenko'
    SEREGA_ID = 588138669
    SEREGA_USERNAME = 'Ironixtemplar'

    @classmethod
    def get_admins_сreads(cls):
        return {
            cls.STAS_ID: cls.STAS_USERNAME,
            cls.SLAVA_ID: cls.SLAVA_USERNAME,
            cls.SEREGA_ID: cls.SEREGA_USERNAME
        }


def add_admin_config(message, keyboard):
    is_admin = False
    unknown_username = message.chat.username
    unknown_user_id = message.chat.id
    admins = Creads.get_admins_сreads()

    for admin_id, admin_username in admins.items():
        if unknown_user_id == admin_id and unknown_username == admin_username:
            is_admin = True
            break

    if is_admin:
        admin_commands = BotActualCommands.get_main_admin_commands()
        for callback_admin_command, admin_command_text in admin_commands.items():
            keyboard.add(types.InlineKeyboardButton(text=admin_command_text, callback_data=callback_admin_command))

