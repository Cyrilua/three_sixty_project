from main.models import Notifications
from main.views.auxiliary_general_methods import *
from datetime import datetime

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


def build_notifications_list(list_notifications):
    result_list = []
    for notification in list_notifications:
        result_notification = {
            'text': notification.name,
            'redirect': notification.redirect,
        }

        if notification.key is not None and notification.key != '':
            result_notification['key'] = notification.key
        result_list.append(result_notification)
    return result_list


def create_notifications(profile: Profile, name: str, type_notification: str, key=None,
                         from_profile=None, on_profile=None) -> None:
    new_notification = Notifications()
    new_notification.url = get_url_from_type(type_notification)
    new_notification.date = datetime.today()
    new_notification.from_profile = from_profile
    new_notification.on_profile = on_profile
    new_notification.name = name
    new_notification.profile = profile
    new_notification.key = key
    new_notification.type = type_notification
    new_notification.save()


def get_url_from_type(type_notification: str):
    if type_notification == 'my_poll':
        return '/result_poll/{}/'
    elif type_notification == 'invite_command':
        return '/invite/t/{}/'
    elif type_notification == 'invite_company':
        return '/invite/c/{}/'
    elif type_notification == 'alien_poll':
        return '/answer_poll/{}/'
    return None
