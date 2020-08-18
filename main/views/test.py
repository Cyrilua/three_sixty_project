from django.shortcuts import redirect
from django.shortcuts import render
from .auxiliary_general_methods import *
from main.models import TestTable, Profile, NeedPassPoll, Poll
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader, Context
from django.contrib.sites.models import Site


def test(request: WSGIRequest):
    poll = Poll.objects.get(id=86)
    print([i.profile for i in NeedPassPoll.objects.filter(poll=poll)])
    mail_subject = 'Новый опрос'
    link = "{}://{}".format(request._get_scheme(), request.get_host()) + '/compiling_poll_link/{}/'.format(poll.key)
    message = render_to_string('main/taking_poll_notifications_email.html', {
        'target': {
            'name': poll.target.name,
            'surname': poll.target.surname
        },
        'link': link
    })
    email = EmailMessage(
        mail_subject, message, to=[i.profile.user.email for i in NeedPassPoll.objects.filter(poll=poll)]
    )
    email.send()
    return render(request, 'main/test.html')
