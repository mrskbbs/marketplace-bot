from typing import Final
from utils import fetchToken

# Fetches token and bot's name
t = fetchToken()
TOKEN: Final = t["TOKEN"]
NAME: Final = t["NAME"]

# Dictinary with all of the bot's messages
CONTENT: Final = {
    "auth": "Чтобы войти. Введите логин и пароль таким образом:\n[ЛОГИН]\n[ПАРОЛЬ]",
    "log_in": "Войти в аккаунт",
    "log_out": "Выход",
    "log_in": "Войти в аккаунт",
    "logged_in": "Вы уже вошли в аккаунт",
    "greet": "Добро пожаловать в бота маркетплейса!",
    "fresh_orders": "Свежие заказы",
    "personal_orders": "Ваши заказы",
    "user_orders":"Заказы пользователя",
    "all_orders": "Все заказы",
    "invalid_auth": "Неверный логин или пароль\nИз окна входа можно выйти с помощтю команды /cancel",
    "input_username": "Введите имя пользователя",
    "input_invalid_username": "Такого пользователя не существует\nВведите имя пользователя снова\nИз окна ввода пользователя можно выйти с помощью команды /cancel",
    "cancel_input_username": "Поиск заказов по имени пользователя был отменён!",
    "cancel_auth": "Вход был отменён!",
    "menu_unauth": "Вы ещё не вошли в аккаунт, хотите войти",
    "menu_staff": "Меню сотрудника {}!\nНажмите на кнопки ниже, чтобы получить информацию о доступных заказах",
    "menu_customer": "Меню покупателя {}!\nНажмите на кнопки ниже, чтобы получить информацию о ваших заказах",
    "goodbye": "До свидания!"
}
