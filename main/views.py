from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from main.models import Profile
from .forms import UserForm, ProfileForm


def user_view(request):
    return render(request, 'main/user.html', {})


def index_view(request):
    return render(request, 'main/index.html', {})


def user_login(request):
    args = {}
    if request.POST:
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user = auth.authenticate(username=username, password=password)
        if user is not None and profile_form.is_valid():
            auth.login(request, user)
            profile_form.save()
            return redirect('/')
        else:
            args['login_error'] = "User has not been found"
            return render(request, 'main/login.html', args)
    else:
        return render(request, 'main/login.html', {})


def user_logout(request):
    auth.logout(request)
    return request('/')


def groups_view(request):
    return render(request, 'main/groups.html', {})
# Create your views here.
