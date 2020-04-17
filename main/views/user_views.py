import copy

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render

from main.forms import ProfileForm


def user_register(request):
    if auth.get_user(request).is_authenticated:
        return redirect('/profile')

    args = {'user_form': UserCreationForm(),
            'profile_form': ProfileForm(),
            'title': "Регистрация"}

    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post['username'] = post['username'].lower()
        user_form = UserCreationForm(post)
        profile_form = ProfileForm(post)

        if user_form.is_valid() and profile_form.is_valid():
            print(request.POST.get('username', ''))
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.user = user
            user.save()
            profile.save()

            # Убрать, если не нужна автоматическая авторизация после регистрации пользователя
            auth.login(request, user)
            return redirect('/')
        else:
            args['user_form'] = user_form
            args['profile_form'] = profile_form
    return render(request, 'main/register.html', args)


def user_login(request):
    if auth.get_user(request).is_authenticated:
        return redirect('/profile')

    args = {'title': "Вход"}

    if request.POST:
        username = request.POST.get("username", '').lower()
        password = request.POST.get("password", '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/profile')
        else:
            args['login_error'] = "Неверный логин или пароль"
            args['username'] = username
            return render(request, 'main/login.html', args)
    return render(request, 'main/login.html', args)


def user_logout(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    auth.logout(request)
    return redirect('/')
