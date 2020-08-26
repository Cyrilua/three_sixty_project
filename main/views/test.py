from django.shortcuts import redirect
from django.shortcuts import render
from django.conf import settings
from .auxiliary_general_methods import *
from main.models import TestTable, Profile, NeedPassPoll, Poll, PlatformCompany
from django.http import JsonResponse
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader, Context
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import get_template


def test(request: WSGIRequest):
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
    return render(request, 'main/test.html')


def open_file(request):
    file = open('/home/ubuntu/code/project360/three_sixty_project/media/media/images/s1200_N0cwvH4.jpg', 'r')
    print(type(file))
    return render(request, 'main/test.html')
