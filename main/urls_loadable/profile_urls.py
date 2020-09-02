from django.urls import path

from ..views.profile_views import render_profile

urlpatterns = [
    # Просмотр профиля
    path('', render_profile.profile_view, name='profile'),
    path('loading', render_profile.loading, name='loading'),
    path('new_notif/', render_profile.new_notification),
    # Удалить приглашение
    path('notification/<int:notification_id>/remove/', render_profile.remove_invite),
    # Отметить уведомления просмотренными
    path('viewing/<int:notification_id>', render_profile.mark_notification_as_viewed),
]
