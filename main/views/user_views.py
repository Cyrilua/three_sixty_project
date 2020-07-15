import copy
from .validators import *

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
        birth_date = datetime.datetime.strptime(post['birthday'], '%d.%m.%Y').date()
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

        elif id_element == 'id_birthday':
           errors = validate_birth_date(date['birthday'])
           return get_result(errors)

        elif id_element == 'id_fullname':
           errors = validate_fullname(date['fullname'])
           return get_result(errors)

        elif id_element == 'id_name':
            errors = validate_name(date['name'])
            return get_result(errors)

        elif id_element == 'id_surname':
            errors = validate_surname(date['surname'])
            return get_result(errors)

        elif id_element == 'id_patronymic':
            errors = validate_patronymic(date['patronymic'])
            return get_result(errors)


def get_result(errors: list):
    if len(errors) == 0:
        return JsonResponse({'resultStatus': 'success'}, status=200)
    return JsonResponse({'resultStatus': 'error',
                         'resultError': errors}, status=200)


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
            count_users = User.objects.filter(username=username)
            if len(count_users) != 0:
                args['error'] = {'password': 'Неверный пароль'}
            else:
                args['error'] = {'login': 'Проверьте правильность логина'}
            args['username'] = username
            return render(request, 'main/no_login/login.html', args)
    return render(request, 'main/no_login/login.html', args)


def user_logout(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    auth.logout(request)
    return redirect('/')
