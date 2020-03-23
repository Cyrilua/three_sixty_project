from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import auth
from .forms import ProfileForm, ProfileAddedForm
from django.contrib.auth import get_user


def user_view(request):
    return render(request, 'main/user.html', {
        "title": "Мой профиль"
    })


def index_view(request):
    return render(request, 'main/index.html', {})


def user_register(request):
    args = {}
    args['user_form'] = UserCreationForm()
    args['profile_form'] = ProfileForm()
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.user = user
            user.save()
            profile.save()
            auth.login(request, user)
            return redirect('/')
        else:
            args['user_form'] = user_form
            args['profile_form'] = profile_form
    return render(request, 'main/register.html', {
        'user_form': args['user_form'],
        'profile_form': args['profile_form'],
        "title": "Регистрация",
    })


def user_login(request):
    args = {
        "title": "Вход",
    }
    if request.POST:
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Логин или пароль неверны"
            return render(request, 'main/login.html', args)
    else:
        return render(request, 'main/login.html', {
            "title": "Вход",
        })


def user_logout(request):
    auth.logout(request)
    return redirect('/')


def groups_view(request):
    return render(request, 'main/groups.html', {
        "title": "Группы"
    })
# Create your views here.
