from django.shortcuts import redirect
from django.shortcuts import render
from . import notifications_views
from .auxiliary_general_methods import *
from main.models import TestTable, Profile, NeedPassPoll
from django.http import JsonResponse


def test(request):
    profile = Profile.objects.get(id=71)
    res = NeedPassPoll.objects.filter(profile=profile).values('profile').values('user')
    print(res)
    for need_pass_poll in res:
        print(need_pass_poll)

    return render(request, 'main/test.html')
