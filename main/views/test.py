from django.shortcuts import redirect
from django.shortcuts import render
from .auxiliary_general_methods import *
from main.models import TestTable, Profile, NeedPassPoll, Poll, PlatformCompany
from django.http import JsonResponse
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader, Context


def test(request: WSGIRequest):
    profile = get_user_profile(request)
    platforms = PlatformCompany.objects.filter(company=profile.company)
    for i in platforms:
        print(i)
    print(platforms)
    return render(request, 'main/test.html')


def open_file(request):
    file = open('/home/ubuntu/code/project360/three_sixty_project/media/media/images/s1200_N0cwvH4.jpg', 'r')
    print(type(file))
    return render(request, 'main/test.html')
