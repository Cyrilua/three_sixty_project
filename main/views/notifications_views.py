from main.models import Notifications, Poll, Group, Company
from main.views.auxiliary_general_methods import *
from datetime import datetime
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist


def redirect_from_notification(request, notification_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        notification = Notifications.objects.get(id=notification_id)
    except ObjectDoesNotExist:
        return redirect('/')

    if get_user_profile(request).id != notification.profile.id:
        return redirect('/')

    url = notification.url.format(notification.key)
    notification.completed = True
    notification.save()
    return redirect(url)


def create_notifications(profile: Profile, name: str, type_notification: str, key=None,
                         from_profile=None, on_profile=None) -> None:
    new_notification = Notifications()
    new_notification.url = _get_url_from_type(type_notification)
    new_notification.date = datetime.today()
    new_notification.from_profile = from_profile
    new_notification.on_profile = on_profile
    new_notification.name = name
    new_notification.profile = profile
    new_notification.key = key
    new_notification.type = type_notification
    new_notification.save()


def _get_url_from_type(type_notification: str):
    if type_notification == 'my_poll':
        return '/result_poll/{}/'
    elif type_notification == 'invite_command':
        return '/invite/t/{}/'
    elif type_notification == 'invite_company':
        return '/invite/c/{}/'
    elif type_notification == 'alien_poll':
        return '/answer_poll/{}/'
    return None


def build_notifications(profile):
    notifications = Notifications.objects.filter(profile=profile)
    my_polls = []
    polls = []
    invites = []
    for notif in notifications:
        _processing_notifications(notif, my_polls, polls, invites)

    return {
        'polls': polls,
        'my_polls': my_polls,
        'invites': invites
    }


def _processing_notifications(notification: Notifications, my_polls: list, polls: list, invites: list) -> None:
    if notification.type == 'my_poll':
        try:
            poll = Poll.objects.get(id=notification.key)
        except ObjectDoesNotExist:
            return None
        collected_notification = _collected_poll_notification(notification, '{} ответов'.format(poll.count_passed))
        my_polls.append(collected_notification)

    elif notification.type == 'invite_company':
        try:
            company = Company.objects.get(key=notification.key)
        except ObjectDoesNotExist:
            return None
        collected_notification = _collected_invite_notification(notification, company.description,
                                                                '/company_view/{}/'.format(company.id))
        invites.append(collected_notification)

    elif notification.type == 'invite_command':
        try:
            command = Group.objects.get(key=notification.key)
        except ObjectDoesNotExist:
            return None
        collected_notification = _collected_invite_notification(notification, command.description,
                                                                '/company_view/{}/'.format(command.id))
        invites.append(collected_notification)
    elif notification.type == 'alien_poll':
        try:
            poll = Poll.objects.get(id=notification.key)
        except ObjectDoesNotExist:
            return None
        collected_notification = _collected_poll_notification(notification, poll.description)
        polls.append(collected_notification)


def _collected_invite_notification(notification: Notifications, description: str, title_url: str) -> dict:
    collected_notification = {
        'url': '/notifications/{}/'.format(notification.id),
        'date': notification.date,
        'title': {
            'name': notification.name,
            'url': title_url,
        },
        'more': {
            'name': "{} {} {}".format(notification.from_profile.surname,
                                      notification.from_profile.name,
                                      notification.from_profile.patronymic),
            'url': '/{}/'.format(notification.from_profile.id)
        },
        'about': description,
        'complited': notification.completed
    }

    return collected_notification


def _collected_poll_notification(notification: Notifications, description: str) -> dict:
    collected_notification = {
        'url': '/notifications/{}/'.format(notification.id),
        'date': notification.date,
        'title': notification.name,
        'more': {
            'name': "{} {} {}".format(notification.from_profile.surname,
                                      notification.from_profile.name,
                                      notification.from_profile.patronymic),
            'url': '/{}/'.format(notification.from_profile.id)
        },
        'about': description,
        'complited': notification.completed
    }

    return collected_notification
