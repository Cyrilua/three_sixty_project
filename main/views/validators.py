import re
import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation, validators
from django.core.validators import EmailValidator
from main.models import Profile
from .auxiliary_general_methods import check_code
import emoji


def validate_login(login: str) -> list:
    print(login)
    result = []
    login = login.lower()
    users = User.objects.all()
    other_users = list(filter(lambda x: x.username == login, users))

    if len(other_users) != 0:
        result.append('Логин уже занят')
    if len(login) < 1:
        result.append('Введите логин')
    if len(login) < 3:
        result.append('Минимальная длинна логина - 3 символа')
    if len(login) > 0 and not login[0].isalpha():
        result.append('Логин должен начинаться с буквы')

    reg = re.compile('[^a-z0-9_]')
    if len(reg.sub('', login)) != len(login) or bool(emoji.get_emoji_regexp().search(login)):
        result.append('Логин содержит запрещенные символы')
    return result


def validate_password1(password: str) -> list:
    result = []
    try:
        password_validation.validate_password(password)
    except ValidationError as error:
        result = error.messages
    if bool(emoji.get_emoji_regexp().search(password)):
        result.append('Пароль содержит запрещенные символы')
    return result


def validate_password2(password2: str, password1: str) -> list:
    result = []
    if password2 != password1:
        result.append('Пароли не совпадают')
    return result


def validate_birth_date(date: str) -> list:
    result = []
    current_date = datetime.datetime.today()
    old_date = datetime.datetime.strptime('1900-1-1', '%Y-%m-%d')
    try:
        birth_date = datetime.datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        result.append('Дата неправильного формата')
        return result

    if birth_date >= current_date or old_date >= birth_date:
        result.append('Некорректная дата')
    return result


def validate_email(email: str) -> list:
    result = []
    if len(email) != 0:
        try:
            email_validator = EmailValidator()
            email_validator(email)
        except ValidationError as error:
            result = error.messages
        users = User.objects.filter(email=email)
        if len(users) != 0:
            result.append('Данный email уже привязан к другоу аккаунту')
    else:
        result.append('Введите значение')
    return result


def validate_name(name: str) -> list:
    result = []
    len_name = len(name)
    if len_name < 2:
        result.append('Слишком короткое имя')
    if len_name > 50:
        result.append('Слишком длинное имя')

    reg = re.compile('[^a-zA-Zа-яА-ЯёЁЙй _]')
    if len(reg.sub('', name)) != len(name):
        result.append('Имя содержит запрещенные символы')
    return result


def validate_surname(surname: str) -> list:
    result = []
    len_name = len(surname)
    if len_name < 2:
        result.append('Слишком короткая фамилия')
    if len_name > 50:
        result.append('Слишком длинная фамилия')

    reg = re.compile('[^a-zA-Zа-яА-ЯёЁЙй _]')
    if len(reg.sub('', surname)) != len(surname):
        result.append('Фамилия содержит запрещенные символы')
    return result


def validate_patronymic(patronymic: str) -> list:
    result = []
    len_name = len(patronymic)
    if len_name < 2:
        result.append('Слишком короткое отчество')
    if len_name > 50:
        result.append('Слишком длинное отчество')

    reg = re.compile('[^a-zA-Zа-яА-ЯёЁЙй _]')
    if len(reg.sub('', patronymic)) != len(patronymic):
        result.append('Отчество содержит запрещенные символы')
    return result


def validate_code(code: str, email: str) -> list:
    result = []
    result_check = check_code(code, email)
    if not result_check:
        result.append('Введен неверный код подтверждения')
    return result


def validate_user_input_in_company_settings(user_input: str) -> bool:
    reg = re.compile('[^a-zA-Zа-яА-ЯёЁЙй _\-0-9.,]')
    return len(reg.sub('', user_input)) == len(user_input) and not bool(emoji.get_emoji_regexp().search(user_input))
