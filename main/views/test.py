from django.shortcuts import redirect
from django.shortcuts import render
from django.conf import settings
from .auxiliary_general_methods import *
from main.models import TestTable, Profile, NeedPassPoll, Poll, PlatformCompany, Group, PositionCompany
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader, Context
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.db.models import Q
from itertools import chain


def test(request: WSGIRequest):
    #_test_send_email(request)
    _test_filter(request)
    return render(request, 'main/test.html')


def _test_send_email(request):
    poll = Poll.objects.filter(id=107).first()
    profile: Profile = get_user_profile(request)
    email = 'aleksandr.korolyov.99@mail.ru'
    mail_subject = 'Новый опрос'
    link = "{}://{}".format(request._get_scheme(), request.get_host()) + \
           '/poll/compiling_poll_link/{}/'.format(poll.key)
    context = {
                'user': {
                    'name': profile.name,
                    'patronymic': profile.patronymic
                },
                'url': link
            }
    message = get_template('main/email/email.html').render(context)
    send_mail(mail_subject, 'dddd', settings.EMAIL_HOST_USER, [email], fail_silently=True, html_message=message)


def _test_filter(request):
    user_input = 'Д'
    profile = get_user_profile(request)
    profiles = Group.objects.filter(id=8).first().profile_set.all()
    result = PositionCompany.objects.filter(company=profile.company)
    print(result)
    temp_result = result.filter(name__istartswith=user_input)
    print(temp_result)
    test1 = temp_result.values_list('profile__id', flat=True)
    print(test1)
    profiles = profiles.filter(id__in=test1)
    print(profiles)

