import copy
import re

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from main.views.profile_views import get_user_profile
from main.forms import ProfileForm, UserChangeEmailForm


from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.core.validators import EmailValidator


def user_register(request):
    if auth.get_user(request).is_authenticated:
        return redirect('/{}/'.format(get_user_profile(request).id))
    print(request.method)
    print(request.is_ajax())


    args = {'user_form': UserCreationForm(),
            'profile_form': ProfileForm(),
            'email_form': UserChangeEmailForm(),
            'title': "Регистрация"}

    if request.method == 'POST':
        print('i am in here')
        post = copy.deepcopy(request.POST)
        post['username'] = post['username'].lower()
        user_form = UserCreationForm(post)
        profile_form = ProfileForm(post)
        email_form = UserChangeEmailForm(post)

        if user_form.is_valid() and profile_form.is_valid() and email_form.is_valid():
            print('all is good')
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.user = user
            user.email = request.POST.get('email', '')

            #    Debug
            # user.save()
            # profile.save()

            # Убрать, если не нужна автоматическая авторизация после регистрации пользователя
            auth.login(request, user)
            return redirect('/')
        else:
            args['user_form'] = user_form
            args['profile_form'] = profile_form
            args['email_form'] = email_form

    if request.is_ajax():
        if request.method == "GET":
            pass
        if request.method == "POST":
            date = request.POST
            print(date)

            if is_button_method(date):
                button_success(date)

            if 'username' in date:
                errors = validate_login(date['username'])
                print(errors)
                return get_result(errors)

            if 'pass2' in date:
                errors = validate_password2(date['pass2'], date['pass1']) # list
                print(errors)
                return get_result(errors)

            if 'pass1' in date:
                errors = validate_password1(date['pass1'])  # list
                print(errors)
                return get_result(errors)

            if 'email' in date:
                errors = validate_email(date['email'])
                return get_result(errors)

    return render(request, 'main/no_login/register.html', args)


def get_result(errors: list):
    if len(errors) == 0:
        return JsonResponse({'resultStatus': 'success'}, status=200)
    return JsonResponse({'resultStatus': 'error',
                         'resultError': errors}, status=200)


def is_button_method(date):
    result = ('username' in date) and ('pass2' in date) and ('pass1' in date) and ('email' in date)
    return result


def button_success(date):
    user = UserCreationForm(date)
    print(user.is_valid())


def validate_login(login: str):
    result = []
    login = login.lower()
    users = User.objects.all()
    other_users = list(filter(lambda x: x.username == login, users))

    if len(other_users) != 0:
        result.append('Имя пользователя уже занято')
    if len(login) < 1:
        result.append('Введите имя пользователя')
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


def validate_email(email: str):
    result = []
    try:
        email_validator = EmailValidator()
        email_validator(email)
    except ValidationError as error:
        result = error.messages
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
