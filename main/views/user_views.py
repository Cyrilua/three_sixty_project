import copy
import re
import datetime

from main.views.auxiliary_general_methods import *

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from main.views.profile_views import get_user_profile
from main.forms import ProfileForm, UserChangeEmailForm, BirthDateForm
from main.models import BirthDate

from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.core.validators import EmailValidator


def user_register(request):
    if auth.get_user(request).is_authenticated:
        return redirect('/{}/'.format(get_user_profile(request).id))

    args = {'user_form': UserCreationForm(),
            'profile_form': ProfileForm(),
            'email_form': UserChangeEmailForm(),
            'birth_date_form': BirthDateForm,
            'title': "Регистрация"}

    if request.is_ajax():
        result_ajax = request_ajax_processing(request)
        if result_ajax is not None:
            return result_ajax

    if request.method == 'POST':
        result_post = request_post_method_processing(request, args)
        if result_post is not None:
            return result_post
    return render(request, 'main/no_login/register.html', args)


def request_post_method_processing(request, args):
    post = copy.deepcopy(request.POST)
    if 'username' in post:
        post['username'] = post['username'].lower()
    user_form = UserCreationForm(post)
    profile_form = ProfileForm(post)
    email_form = UserChangeEmailForm(post)
    if user_form.is_valid() and profile_form.is_valid() and email_form.is_valid():
        user = user_form.save(commit=False)
        profile = profile_form.save(commit=False)
        profile.user = user
        user.email = request.POST.get('email', '')
        user.save()
        profile.save()
        birth_date = datetime.datetime.strptime(post['birthday'], '%Y-%m-%d').date()
        date = BirthDate()
        date.birthday = birth_date
        date.profile = profile
        date.save()

        # Убрать, если не нужна автоматическая авторизация после регистрации пользователя
        auth.login(request, user)
        send_email_validate_message(request)
        return redirect('/')
    else:
        args['user_form'] = user_form
        args['profile_form'] = profile_form
        args['email_form'] = email_form


def request_ajax_processing(request):
    if request.method == "GET":
        pass
    if request.method == "POST":
        date = request.POST
        id_element = date['id']

        if id_element == 'id_username':
            errors = validate_login(date['username'])
            return get_result(errors)

        elif id_element == 'id_password2':
            errors = validate_password2(date['password2'], date['password1'])  # list
            return get_result(errors)

        elif id_element == 'id_password1':
            errors = validate_password1(date['password1'])  # list
            return get_result(errors)

        elif id_element == 'id_email':
            errors = validate_email(date['email'])
            return get_result(errors)

        ########## Раскомментировать по готовности. Проверить правильность названий аргументов ############
        #elif id_element == 'id_birthday':
        #    errors = validate_birth_date(date['birthday'])
        #    return get_result(errors)

        #elif id_element == 'id_fullname':
        #    errors = validate_fullname(date['fullname'])
        #    return get_result(errors)


def get_result(errors: list):
    if len(errors) == 0:
        return JsonResponse({'resultStatus': 'success'}, status=200)
    return JsonResponse({'resultStatus': 'error',
                         'resultError': errors}, status=200)


def validate_login(login: str):
    result = []
    login = login.lower()
    users = User.objects.all()
    other_users = list(filter(lambda x: x.username == login, users))

    if len(other_users) != 0:
        result.append('Имя пользователя уже занято')
    if len(login) < 1:
        result.append('Введите имя пользователя')
    if len(login) < 3:
        result.append('Минимальная длинна логина - 3 символа')

    reg = re.compile('[^a-z0-9_]')
    if len(reg.sub('', login)) != len(login):
        result.append('Логин содержит запрещенные символы')

    return result


def validate_password1(password: str):
    result = []
    try:
        password_validation.validate_password(password)
    except ValidationError as error:
        result = error.messages
    return result


def validate_password2(password2: str, password1: str):
    result = []
    if password2 != password1:
        result.append('Пароли не совпадают')
    return result


def validate_birth_date(date: str):
    result = []
    current_date = datetime.datetime.today()
    old_date = datetime.datetime.strptime('1900-1-1', '%Y-%m-%d')
    try:
        birth_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        result.append('Дата неправильного формата')
        return result
    if birth_date >= current_date or old_date <= birth_date:
        result.append('Некорректная дата')
    return result


def validate_email(email: str):
    result = []
    try:
        email_validator = EmailValidator()
        email_validator(email)
    except ValidationError as error:
        result = error.messages
    users = User.objects.filter(email=email)
    if len(users) != 0:
        result.append('Данный email уже привязан к другоу аккаунту')
    return result


def validate_fullname(name: str):
    result = []
    len_name = len(name)
    if len_name < 6:
        result.append('Введенное имя слишком короткое. Оно должно содержать минимум 6 символа')
    if len_name > 150:
        result.append('Введенное имя слишком длинное. Оно должно состоять не более чем из 150 символов')

    # убрать проверку на запрещенные символы при необходимости
    reg = re.compile('[^a-zA-Zа-яА-ЯёЁЙй _]')
    if len(reg.sub('', name)) != len(name):
        result.append('Имя содержит запрещенные символы')
    return result


def user_login(request):
    if auth.get_user(request).is_authenticated:
        profile = get_user_profile(request)
        return redirect('/{}/'.format(profile.id))

    args = {'title': "Вход"}

    if request.POST:
        username = request.POST.get("username", '').lower()
        password = request.POST.get("password", '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/{}/'.format(get_user_profile(request).id))
        else:
            args['login_error'] = "Неверный логин или пароль"
            args['username'] = username
            return render(request, 'main/no_login/login.html', args)
    return render(request, 'main/no_login/login.html', args)


def user_logout(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    auth.logout(request)
    return redirect('/')
