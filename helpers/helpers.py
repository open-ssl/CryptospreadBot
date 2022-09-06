import sys
from traceback import print_exception
from telebot import types
from time import sleep
from requests_futures import sessions


API_TOKEN = '5686307192:AAGWxHH_auacIqrN6gXK2F3cBKJnpFqdXyg'
GENERATED_CODE_LENGTH = 16
# CREATE_NEW_CODE_END_POINT = 'http://cryptospread.net/create_code_for_user'
CREATE_NEW_CODE_END_POINT = 'http://127.0.0.1:5002/create_code_for_user'
# CREATE_NEW_ACCESS_END_POINT = 'http://cryptospread.net/create_new_access'
CREATE_NEW_ACCESS_END_POINT = 'http://127.0.0.1:5002/create_new_access'


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


class BotActualCommands:
    GET_ACCESS_KEY_COMMAND = 'get_access_key'
    WRITE_DEVELOPERS_COMMAND = 'write_developers'
    BUY_ACCESS_COMMAND = 'buy_access'
    USER_PAID_ACCESS = 'user_paid_access'
    MAIN_MENU = 'main_menu'
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
            cls.GET_ACCESS_KEY_COMMAND: Message.GET_TRIAL_KEY,
            cls.BUY_ACCESS_COMMAND: Message.BUY_ACCESS,
            cls.WRITE_DEVELOPERS_COMMAND: Message.WRITE_US,
        }

    @classmethod
    def get_all_commands(cls):
        return {
            cls.GET_ACCESS_KEY_COMMAND: Message.GET_TRIAL_KEY,
            cls.BUY_ACCESS_COMMAND: Message.BUY_ACCESS,
            cls.WRITE_DEVELOPERS_COMMAND: Message.WRITE_US,
            cls.USER_PAID_ACCESS: Message.USER_PAID_ACCESS,
            cls.MAIN_MENU: Message.MAIN_MENU
        }

    @classmethod
    def get_commands_for_pay(cls):
        return {
            cls.USER_PAID_ACCESS: Message.USER_PAID_ACCESS,
            cls.MAIN_MENU: Message.MAIN_MENU
        }

    @classmethod
    def get_main_admin_commands(cls):
        return {
            cls.ADMIN_SECTION: Message.ADMIN_NAME,
        }

    @classmethod
    def get_all_admin_commands(cls):
        return {
            cls.ADMIN_SECTION: Message.ADMIN_NAME,
            cls.ADD_ACCESS_FOR_USER: Message.ADD_SUB,
            cls.ANSWER_FOR_USER: Message.ANSWER_FOR_USERS,
            cls.ADD_ACCESS_WITH_TELEGRAM: Message.ADD_WITH_TELEGRAM,
            cls.ADD_ACCESS_WITH_EMAIL: Message.ADD_WITH_EMAIL
        }

    @classmethod
    def get_admin_commands_level2(cls):
        return {
            cls.ADD_ACCESS_FOR_USER: Message.ADD_SUB,
            cls.ANSWER_FOR_USER: Message.ANSWER_FOR_USERS,
        }

    @classmethod
    def get_admin_commands_level3(cls):
        return {
            cls.ADD_ACCESS_WITH_TELEGRAM: Message.ADD_WITH_TELEGRAM,
            cls.ADD_ACCESS_WITH_EMAIL: Message.ADD_WITH_EMAIL,
        }


class Const:
    GENERATED_CODE = 'generatedCode'
    TELEGRAM_USER = 'telegramUser'
    EMAIL = 'email'
    TELEGRAM = 'telegram'

    ORERATION_RESULT = 'operationResult'
    EXTRA_DATA = 'extraData'
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

    @classmethod
    def get_admins_сreads(cls):
        return {
            cls.STAS_ID: cls.STAS_USERNAME,
            cls.SLAVA_ID: cls.SLAVA_USERNAME
        }


class Message:
    START_BOT_MESSAGE = "Привет {}! \nВы написали боту команды cryptospread.net\nВыберите действие"
    UNKNOWN_ACTION_MESSAGE = "Вы ввели неизвестный текст или команду. Введите корректное значение или запустите /start"
    BUY_ACCESS_MESSAGE = "Здесь будет информация о том, как купить подписку.\n" \
                         "Типы доступа:\n" \
                         "3 копейки - 1 день\n" \
                         "2 рубля - 1 неделя\n" \
                         "2 рубля 3 копейки - 1 месяц\n" \
                         "Далее, Вам необходимо будет указать юзера который произвел оплату\n" \
                         "Мы проверим оплаченную вами сумму и в зависимости от ее количества выдадим вам нужный доступ\n" \
                         "\nПосле оплаты нажмите на кнопку 'Оплачено'"
    CHECK_USER_FOR_CODE_MESSAGE = "Делаем проверку Вашего юзера для выдачи кода..."
    WRITE_DEVELOPERS_MESSAGE = "Напишите нам и мы Вам обязательно ответим в ближайшее время!"
    SUCCESS_GENERATED_CODE_MESSAGE = "Для вас сгенерирован код для одного дня бесплатного доступа!\n" \
                                     "Ваш код - {0} \n" \
                                     "Активируйте его в личном кабинете"
    ERROR_MESSAGE = "Для вашего пользователя невозможно выполнить данное действие\n" \
                    "Пожалуйста, напишите команде поддержки и мы решим эту проблему"
    ADMIN_SECTION_GREETING = "Разделяй и влавствуй)\nВыбери дальнейшее действие"
    ADD_ACCESS_FOR_USER_GREETING = "Выбираем через что добавляем пользователя"
    ANSWER_FOR_USER_GREETING = "Здесь будем отвечать пользователям с поддержки"
    AFTER_USER_PAID_ACCESS = "Введите, пожалуйста, имя юзера с которого производилась оплата.\n" \
                             "Мы проверим оплаченную вами сумму и в зависимости от ее количества выдадим вам нужный доступ"
    INPUT_TELEGRAM_USER_FOR_ACCESS = "Введите тип подписки и телеграм никнейм юзера для добавления\n" \
                                     "Пример: 1 NickName"
    INPUT_EMAIL_USER_FOR_ACCESS = "Введите тип подписки и почту юзера для добавления\n" \
                                  "Пример: 1 mail@mail.ru"

    ####################################################################
    GET_TRIAL_KEY = 'Получить пробный ключ'
    BUY_ACCESS = 'Купить подписку'
    WRITE_US = 'Написать команде'
    ADMIN_NAME = 'Админка'
    ADD_SUB = 'Добавить подписку'
    ANSWER_FOR_USERS = 'Ответить в поддержку'
    ADD_WITH_TELEGRAM = 'Добавить через телеграм'
    ADD_WITH_EMAIL = 'Добавить через почту'

    USER_PAID_ACCESS = 'Оплачено'
    MAIN_MENU = 'В главное меню'
    ############################################################################


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

