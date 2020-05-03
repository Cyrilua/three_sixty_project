from main.models import Notifications
from main.views.auxiliary_general_methods import *


def redirect_from_notifications(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    list_notifications = Notifications.objects.filter(profile=profile)
    args = {
        'title': 'Уведомления',
        'notifications': build_notifications_list(list_notifications)
    }
    return render(request, 'main/notifications.html', args)


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


def add_notification(profile, name, redirect_name, key=None):
    new_notification = Notifications()
    new_notification.profile = profile
    new_notification.redirect = redirect_name
    new_notification.name = name
    if key is not None:
        new_notification.key = key
    new_notification.save()
