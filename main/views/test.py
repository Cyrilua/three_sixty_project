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
    platforms = PlatformCompany.objects.filter(company=profile.company)
    for i in platforms:
        print(i)
    print(platforms)
    return render(request, 'main/test.html')
