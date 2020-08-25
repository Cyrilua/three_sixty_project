from django.shortcuts import redirect
from django.shortcuts import render
from .auxiliary_general_methods import *
from main.models import TestTable, Profile, NeedPassPoll, Poll, PlatformCompany
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader, Context
from django.http import JsonResponse


def test(request: WSGIRequest):
    profile = get_user_profile(request)
    print(type(profile) == Profile)
    print(type(profile) is Profile)
    print(type(profile))
    print(profile is Profile())
    return render(request, 'main/test.html')
