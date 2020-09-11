from django.shortcuts import redirect
from django.shortcuts import render
from django.conf import settings
from .auxiliary_general_methods import *
from main.models import TestTable, Profile, NeedPassPoll, Poll, PlatformCompany, Group, PositionCompany, ProfilePhoto, Questions
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader, Context
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.db.models import Q
from itertools import chain
from django.utils.html import escape
from .poll_views.create_poll import _sending_emails

from django.contrib.sites.shortcuts import get_current_site


def test(request: WSGIRequest):
    return render(request, 'main/test.html')


def _sending_emails1(request: WSGIRequest, poll: Poll):
    for need_pass in NeedPassPoll.objects.filter(poll=poll):
        need_pass: NeedPassPoll
        email = "aleksandr.korolyov.99@mail.ru"
        mail_subject = 'Новый опрос'
        link = "1234"

        context = {
            'type_email': 'verification',
            'user': {
                'name': poll.target.name,
                'patronymic': poll.target.patronymic
            },
            'code': link
        }
        message = get_template('main/email/email.html').render(context)
        send_mail(mail_subject, 'dddd', settings.EMAIL_HOST_USER, [email], fail_silently=True, html_message=message)


def get_url_host(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    host = escape(request.get_host())
    return '%s://%s' % (protocol, host)


def _delete_companies(request: WSGIRequest):
    poll = Poll.objects.filter(id=113)
    print(type(poll.first()) == Poll)


def _test_send_email(request):
    poll = Poll.objects.filter(id=107).first()
    profile: Profile = get_user_profile(request)
    email = 'aleksandr.korolyov.99@mail.ru'
    mail_subject = 'Новый опрос'
    link = "{}://{}".format(request._get_scheme(), request.get_host()) + \
           '/poll/compiling_poll_link/{}/'.format(poll.key)
    context = {
                'type_email': 'notification',
                'user': {
                    'name': profile.name,
                    'patronymic': profile.patronymic
                },
                'url': link
            }
    message = get_template('main/email/email.html').render(context)
    send_mail(mail_subject, 'dddd', settings.EMAIL_HOST_USER, [email], fail_silently=True, html_message=message)


def _test_filter(request):
    team = Group.objects.get(id=8)
    profile = get_user_profile(request)
    user_input = ['Д']
    company = profile.company
    profiles = team.profile_set.all()
    for input_iter in user_input:
        profiles = profiles.filter(
            Q(name__istartswith=input_iter) |
            Q(surname__istartswith=input_iter) |
            Q(patronymic__istartswith=input_iter))
        if company is not None:
            id_profiles_by_positions = PositionCompany.objects \
                .filter(company=company) \
                .filter(name__istartswith=input_iter) \
                .values_list('profile__id', flat=True)
            print(id_profiles_by_positions)
            profiles_by_positions = Profile.objects.filter(id__in=id_profiles_by_positions)
            print(profiles_by_positions)
            id_profiles_by_platforms = PlatformCompany.objects \
                .filter(company=company) \
                .filter(name__istartswith=input_iter) \
                .values_list('profile__id', flat=True)
            print(id_profiles_by_platforms)
            profiles_by_platforms = Profile.objects.filter(id__in=id_profiles_by_platforms)
            print(profiles_by_platforms)
            profiles = profiles.union(profiles_by_platforms, profiles_by_positions)
    print(profiles)

