from django.shortcuts import redirect
from django.shortcuts import render
from . import notifications_views
from .auxiliary_general_methods import *
from main.models import TestTable
from django.http import JsonResponse
from django.conf import settings


def code_verifications_test(request):
    code = '98765'
    code_md5 = hashlib.md5()
    code_md5.update(code.encode('utf-8'))
    result = code_md5.digest()
    print(result)
    test_table = TestTable()
    test_table.code = str(result)
    test_table.save()
    get: TestTable = TestTable.objects.get(id=3)
    print(get.code)
    print(type(get.code))
    return render(request, 'main/test.html')


def open_file(request):
    file = open('/home/ubuntu/code/project360/three_sixty_project/media/media/images/s1200_N0cwvH4.jpg', 'r')
    print(type(file))
    return render(request, 'main/test.html')
