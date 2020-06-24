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
    if request.is_ajax():
        if request.method == "GET":
            pass
        if request.method == "POST":
            date = request.POST
            print(date)

            if is_button_method(date):
                button_success(date)

            if 'username' in date:
                if validate_login(date['username']):
                    return JsonResponse({'usernameStatus': 'success'}, status=200)
                return JsonResponse({'usernameStatus': 'error',
                                     'usernameError': 'Ошибка о чем то'}, status=200)

            if 'pass2' in date:
                errors = validate_password2(date['pass2'], date['pass1']) # list
                if len(errors) == 0:
                    return JsonResponse({'password2Status': 'success'}, status=200)
                return JsonResponse({'password2Status': 'error',
                                     'password2Error': errors}, status=200)

            if 'pass1' in date:
                errors = validate_password1(date['pass1'])  # list
                if len(errors) == 0:
                    return JsonResponse({'password1Status': 'success'}, status=200)
                return JsonResponse({'password1Status': 'error',
                                     'password1Error': errors}, status=200)

            if 'email' in date:
                errors = validate_email(date['email'])
                if len(errors) == 0:
                    return JsonResponse({'emailStatus': 'success'}, status=200)
                return JsonResponse({'emailStatus': 'error',
                                     'emailError': errors}, status=200)

    args = {'user_form': UserCreationForm(),
            'profile_form': ProfileForm(),
            'email_form': UserChangeEmailForm(),
            'title': "Регистрация"}
    return render(request, 'main/no_login/register.html', args)


def is_button_method(date):
    result = ('username' in date) and ('pass2' in date) and ('pass1' in date) and ('email' in date)
    return result


def button_success(date):
    user = UserCreationForm(date)
    print(user.is_valid())


def validate_login(login: str):
    login = login.lower()
    users = User.objects.all()
    result = list(filter(lambda x: x.username == login, users))
    print(result)
    return len(result) == 0 and len(login) > 0


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
