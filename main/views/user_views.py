import copy

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render

from main.views.profile_views import get_user_profile
from main.forms import ProfileForm, UserChangeEmailForm


def user_register(request):
    if auth.get_user(request).is_authenticated:
        return redirect('/{}/'.format(get_user_profile(request).id))

    args = {'user_form': UserCreationForm(),
            'profile_form': ProfileForm(),
            'email_form': UserChangeEmailForm(),
            'title': "Регистрация"}

    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
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

            # Убрать, если не нужна автоматическая авторизация после регистрации пользователя
            auth.login(request, user)
            return redirect('/')
        else:
            args['user_form'] = user_form
            args['profile_form'] = profile_form
            args['email_form'] = email_form
    return render(request, 'main/no_login/register.html', args)


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
