from django.shortcuts import redirect
from django.shortcuts import render
from . import notifications_views
from .auxiliary_general_methods import *
from main.models import TestTable, Questions
from django.http import JsonResponse


def test(request):
    settings = Questions.objects.get(id=14)
    settings.delete()
    return render(request, 'main/test.html')
