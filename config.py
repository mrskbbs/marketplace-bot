from typing import Final
# from utils import fetchTokens


def fetchTokens() -> tuple[str, str]:
    """
    Fetches data from .tokens file: 
     - First line is bot's token.
     - Second line is bot's name
    """
    d: dict = dict()

    with open(".tokens", "r", encoding = "utf-8") as f:
        for line in f:
            try:
                key, val = line.split("=")
                d[key.strip()] = val.strip()
            except ValueError:
                continue

    return d

# Fetches tokens from .tokens file
TOKENS: Final = fetchTokens()

# Dictinary with all of the bot's messages
CONTENT: Final = {
    "auth": "Чтобы войти. Введите почту и пароль таким образом:\n[ПОЧТА]\n[ПАРОЛЬ]",
    "log_in": "Войти в аккаунт",
    "log_out": "Выход",
    "log_in": "Войти в аккаунт",
    "logged_in": "Вы уже вошли в аккаунт",
    "greet": "Добро пожаловать в бота маркетплейса!",
    "fresh_orders": "Свежие заказы",
    "personal_orders": "Ваши заказы",
    "user_orders":"Заказы пользователя",
    "all_orders": "Все заказы",
    "invalid_auth": "Неверная почта или пароль\nИз окна входа можно выйти с помощью команды /cancel",
    "input_username": "Введите id пользователя, или id нескольких пользователей через запятую",
    "input_invalid_username": "Такого пользователя не существует, либо этот пользователь ещё ничего не заказал\nВведите id пользователя снова\nИз окна ввода id пользователя можно выйти с помощью команды /cancel",
    "cancel_input_username": "Поиск заказов по id пользователя был отменён!",
    "cancel_auth": "Вход был отменён!",
    "menu_unauth": "Вы ещё не вошли в аккаунт, хотите войти",
    "menu_staff": "<u>Меню сотрудника {}</u>\nНажмите на кнопки ниже, чтобы получить информацию о доступных заказах",
    "menu_customer": "<u>Меню покупателя {}</u>\nНажмите на кнопки ниже, чтобы получить информацию о ваших заказах",
    "menu_back": "Назад в меню",
    "goodbye": "До свидания!"
}
