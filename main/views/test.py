from django.shortcuts import redirect
from django.shortcuts import render
from . import notifications_views
from .auxiliary_general_methods import *
from main.models import TestTable, Profile
from django.http import JsonResponse


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
