from django.shortcuts import redirect
from django.shortcuts import render

from main.models import Notifications
from main.views.auxiliary_general_methods import *


def redirect_from_notifications(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    list_notifications = Notifications.objects.filter(profile=profile)
    args = {
        'Уведомления'
        'profile': profile,
        'list_notifications': list_notifications
    }
    if request.method == "POST":
        notification_id = request.POST.get('id_notification', '')
        try:
            notification = Notifications.objects.get(id=notification_id)
            url_redirect = notification.redirect
            return redirect(url_redirect)
        except:
            args['error'] = 'Этого уведомления не существует'
    return render(request, 'main/notifications.html', args)
