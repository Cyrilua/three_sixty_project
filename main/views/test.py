from django.shortcuts import redirect
from django.shortcuts import render
from . import notifications_views
from .auxiliary_general_methods import *
from main.models import TestTable, Profile, NeedPassPoll, Poll
from django.http import JsonResponse


def test(request):
    poll = Poll.objects.get(id=61)
    result = [i.profile.user.email for i in NeedPassPoll.objects.filter(poll=poll)]
    print(result)
    return render(request, 'main/test.html')
