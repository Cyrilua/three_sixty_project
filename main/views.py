from django.shortcuts import render
from django.http import HttpResponse


def user_view(request):
    return render(request, 'main/user.html', {})


def index_view(request):
    return render(request, 'main/index.html', {})
# Create your views here.
