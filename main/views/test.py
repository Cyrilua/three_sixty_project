from django.shortcuts import redirect
from django.shortcuts import render
from . import notifications_views
from .auxiliary_general_methods import *
from main.models import TestTable, Profile, NeedPassPoll, Poll
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader, Context
from django.contrib.sites.models import Site


def test(request: WSGIRequest):
    poll = Poll.objects.get(id=86)
    mail_subject = 'Новый опрос'
    link = "{}://{}".format(request._get_scheme(), request.get_host()) + '/compiling_poll_link/{}/'.format(poll.key)
    message = render_to_string('main/taking_poll_notifications_email.html', {
        'target': {
            'name': poll.target.name,
            'surname': poll.target.surname
        },
        'link': link
    })
    emails = [i.profile.user.email for i in NeedPassPoll.objects.filter(poll=poll)]
    print(emails)
    email = EmailMessage(
        mail_subject, message, to=emails
    )
    return render(request, 'main/test.html')
