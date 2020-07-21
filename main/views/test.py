from django.shortcuts import redirect
from django.shortcuts import render
from . import notifications_views
from .auxiliary_general_methods import *
from main.models import Profile
from django.http import JsonResponse


def create_notifications(request):
    key = '78d0a42e-4224-47c2-9479-a5c411fd1a12'
    profile = Profile.objects.get(id=95)
    notifications_views.create_notifications(get_user_profile(request), 'Тестовое уведомление', 'invite_command',
                                             key=key, from_profile=profile)
    return redirect('/')


def test_ajax_request(request):
    print('i am here')
    return JsonResponse({}, status=200)
