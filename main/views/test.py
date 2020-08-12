from django.shortcuts import redirect
from django.shortcuts import render
from . import notifications_views
from .auxiliary_general_methods import *
from main.models import TestTable, Profile
from django.http import JsonResponse
from django.conf import settings


def test(request):
    profiles = Profile.objects.all()
    number = 1
    for profile in profiles:
        if profile.surname is None or profile.surname == '':
            profile.surname = 'Surname{}'.format(number)
            profile.patronymic = 'Patronymic{}'.format(number)
            profile.save()
            number += 1
            print(number)
    return render(request, 'main/test.html')


def open_file(request):
    file = open('/home/ubuntu/code/project360/three_sixty_project/media/media/images/s1200_N0cwvH4.jpg', 'r')
    print(type(file))
    return render(request, 'main/test.html')
