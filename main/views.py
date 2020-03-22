from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from main.models import Profile
from .forms import ProfileForm


def user_view(request):
    return render(request, 'main/user.html', {})


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
            user_form.save()
            profile_form.save()
            auth.login(request, user_form)
            return redirect('')
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
            args['login_error'] = "User has not been found"
            return render(request, 'main/login.html', args)
    else:
        return render(request, 'main/login.html', {
            "title": "Вход",
        })


def user_logout(request):
    auth.logout(request)
    return redirect('/')


def groups_view(request):
    return render(request, 'main/groups.html', {})
# Create your views here.
