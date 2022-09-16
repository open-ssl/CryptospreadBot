""" Модуль с константами """

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
    ALEX_ID = 369618248
    ALEX_USERNAME = 'Petryanin'

    @classmethod
    def get_admins_creads(cls):
        return {
            cls.STAS_ID: cls.STAS_USERNAME,
            cls.SLAVA_ID: cls.SLAVA_USERNAME,
            cls.ALEX_ID: cls.ALEX_USERNAME,
        }


class UserMessage:
    """ Сообщения от пользователя """

    _EMOJI_KEY = '\U0001F511'
    _EMOJI_DOLLAR = '\U0001F4B5'
    _EMOJI_MEMO = '\U0001F4DD'
    _EMOJI_GEAR = '\U00002699'
    _EMOJI_LOUDSPEAKER = '\U0001F4E2'
    _EMOJI_NEW = '\U0001F195'
    _EMOJI_CHECK_MARK = '\U00002705'
    _EMOJI_LEFT_ARROW = '\U00002B05'
    _EMOJI_HOUSE = '\U0001F3E0'

    GET_TRIAL_KEY = _EMOJI_KEY + 'Получить пробный ключ'
    BUY_ACCESS = _EMOJI_DOLLAR + 'Купить подписку'
    WRITE_US = _EMOJI_MEMO + 'Написать команде'
    ADMIN_NAME = _EMOJI_GEAR + 'Админка'
    ADD_SUB = _EMOJI_NEW + 'Добавить подписку'
    ANSWER_FOR_USERS = _EMOJI_LOUDSPEAKER + 'Ответить в поддержку'
    ADD_WITH_TELEGRAM = 'Добавить через телеграм'
    ADD_WITH_EMAIL = 'Добавить через почту'

    USER_PAID_ACCESS = _EMOJI_CHECK_MARK + 'Оплачено'
    MAIN_MENU = _EMOJI_HOUSE + 'В главное меню'
    CANCEL = _EMOJI_LEFT_ARROW + 'Отмена'

    @classmethod
    def get_main_menu_commands(cls) -> tuple:
        """ Команды главного меню """
        return (
            UserMessage.GET_TRIAL_KEY,
            UserMessage.BUY_ACCESS,
            UserMessage.WRITE_US,
        )

    @classmethod
    def get_all_commands(cls):
        """ Все команды """
        return (
            UserMessage.GET_TRIAL_KEY,
            UserMessage.BUY_ACCESS,
            UserMessage.WRITE_US,
            UserMessage.USER_PAID_ACCESS,
            UserMessage.ADMIN_NAME,
            UserMessage.ANSWER_FOR_USERS,
            UserMessage.ADD_WITH_TELEGRAM,
            UserMessage.ADD_WITH_EMAIL,
            UserMessage.MAIN_MENU,
            UserMessage.CANCEL,
        )

    @classmethod
    def get_commands_for_pay(cls):
        """ Команды для меню покупки подписки """
        return (
            UserMessage.USER_PAID_ACCESS,
            UserMessage.MAIN_MENU,
        )

    @classmethod
    def get_all_admin_commands(cls):
        """ Все команды админки """
        return (
            UserMessage.ADMIN_NAME,
            UserMessage.ADD_SUB,
            UserMessage.ANSWER_FOR_USERS,
            UserMessage.ADD_WITH_TELEGRAM,
            UserMessage.ADD_WITH_EMAIL,
            UserMessage.MAIN_MENU,
        )

    @classmethod
    def get_main_admin_commands(cls):
        """ Основные команды админки """
        return (
            UserMessage.ADD_SUB,
            UserMessage.ANSWER_FOR_USERS,
            UserMessage.MAIN_MENU,
        )

    @classmethod
    def get_admin_commands_for_adding_user(cls):
        """ Команды добавления пользователя """
        return (
            UserMessage.ADD_WITH_TELEGRAM,
            UserMessage.ADD_WITH_EMAIL,
            UserMessage.CANCEL,
            UserMessage.MAIN_MENU,
        )


class BotMessage:
    """ Сообщения от бота """

    START_BOT_MESSAGE = "Привет {}! \nВы написали боту команды cryptospread.net\nВыберите действие"
    UNKNOWN_ACTION_MESSAGE = "Вы ввели неизвестный текст или команду. Введите корректное значение или запустите /start"
    BUY_ACCESS_MESSAGE = "Здесь будет информация о том, как купить подписку.\n" \
                         "Типы доступа:\n" \
                         "3 копейки - 1 день\n" \
                         "2 рубля - 1 неделя\n" \
                         "2 рубля 3 копейки - 1 месяц\n" \
                         "Далее, Вам необходимо будет указать юзера, который произвел оплату\n" \
                         "Мы проверим оплаченную вами сумму и в зависимости от " \
                         "ее количества выдадим вам нужный доступ\n" \
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
                             "Мы проверим оплаченную вами сумму и в зависимости от " \
                             "ее количества выдадим вам нужный доступ"
    INPUT_TELEGRAM_USER_FOR_ACCESS = "Введите тип подписки и телеграм никнейм юзера для добавления\n" \
                                     "Пример: 1 NickName"
    INPUT_EMAIL_USER_FOR_ACCESS = "Введите тип подписки и почту юзера для добавления\n" \
                                  "Пример: 1 mail@mail.ru"
    SUCCESS_ACCESS_FOR_USER = "Доступ для аккаунта с {} {} успешно добавлен"

    SAMPLE_TEXT = "Спасибо, что что-то ввели!"
