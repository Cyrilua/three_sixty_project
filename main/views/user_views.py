import copy

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse

from main.views.profile_views import get_user_profile
from main.forms import ProfileForm, UserChangeEmailForm


def user_register(request):
    if auth.get_user(request).is_authenticated:
        return redirect('/{}/'.format(get_user_profile(request).id))
    if request.is_ajax():
        if request.method == "GET":
            pass
        if request.method == "POST":
            date = request.POST
            print(date)
            if 'username' in date:
                if validate_login(date['username']):
                    return JsonResponse({'resultStatus': 'success'}, status=200)
                return JsonResponse({'resultStatus': 'error',
                                     'resultError': 'Ошибка о чем то'}, status=200)
            if 'pass1' in date:
                if validate_password1(date['pass1']):
                    return JsonResponse({'resultStatus': 'success'}, status=200)
                return JsonResponse({'resultStatus': 'error',
                                     'resultError': 'Ошибка о чем то'}, status=200)
            if 'pass2' in date:
                if validate_password2(date['pass2'], date['pass1']):
                    return JsonResponse({'resultStatus': 'success'}, status=200)
                return JsonResponse({'resultStatus': 'error',
                                     'resultError': 'Ошибка о чем то'}, status=200)

    args = {'user_form': UserCreationForm(),
            'profile_form': ProfileForm(),
            'email_form': UserChangeEmailForm(),
            'title': "Регистрация"}
    user = UserCreationForm(request.POST)
    user.is_valid()

    return render(request, 'main/no_login/register.html', args)


def validate_login(login:str):
    return True


def validate_password1(password:str):
    return True


def validate_password2(password2:str, password1:str):
    return True


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
