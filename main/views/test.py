from django.shortcuts import redirect
from django.shortcuts import render
from . import notifications_views, auxiliary_general_methods


def create_notifications(request):
    notifications_views.create_notifications()
