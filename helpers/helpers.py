from time import sleep
from requests_futures import sessions


API_TOKEN = '5686307192:AAGWxHH_auacIqrN6gXK2F3cBKJnpFqdXyg'
START_BOT_MESSAGE = "Привет {}! \nВы написали боту команды cryptospread.net.\nВыберите действие:"
UNKNOWN_ACTION_MESSAGE = "Вы ввели неизвестный текст или команду. Введите корректное значение или запустите /start"
GENERATED_CODE_LENGTH = 16
BUY_ACCESS_MESSAGE = "Здесь будет информация о том, как купить подписку"
CHECK_USER_FOR_CODE_MESSAGE = "Делаем проверку Вашего юзера для выдачи кода..."
# CREATE_NEW_CODE_END_POINT = 'cryptospread.net/create_code_for_user'
CREATE_NEW_CODE_END_POINT = 'http://127.0.0.1:5002/create_code_for_user'
WRITE_DEVELOPERS_MESSAGE = "Напишите нам и мы Вам обязательно ответим в ближайшее время!"
SUCCESS_GENERATED_CODE_MESSAGE = "Для вас сгенерирован код для одного дня бесплатного доступа!\n" \
                                 "Ваш код - {0} \n" \
                                 "Активируйте его в личном кабинете"


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

    @classmethod
    def get_all_commands(cls):
        return {
            cls.GET_ACCESS_KEY_COMMAND: 'Получить пробный ключ',
            cls.BUY_ACCESS_COMMAND: 'Купить подписку',
            cls.WRITE_DEVELOPERS_COMMAND: 'Написать команде'
        }


class Const:
    GENERATED_CODE = 'generatedCode'
    TELEGRAM_USER = 'telegramUser'
    ORERATION_RESULT = 'operationResult'
    EXTRA_DATA = 'extraData'