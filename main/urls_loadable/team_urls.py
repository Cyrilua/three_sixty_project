from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from ..views.teams import team_views

urlpatterns = [
    # Промотр конкретной команды
    path('', team_views.team_view, name='team_view'),
    # Настройки команды
    path('settings/', team_views.team_settings_view, name='team_setting'),
    # Удаление команды
    path('settings/remove/', team_views.team_remove, name='team_remove'),
    # Удаление команды
    path('settings/change/', team_views.team_change, name='team_change'),
    # Получить ссылку для вступления в команду
    path('settings/get_link_invite/', team_views.get_invite_link),
    # Поиск
    path('search/', team_views.search_teammate, name='search'),
    # Приглашение новых участников через команду
    path('invites/', team_views.team_new_invites, name='team_new_invites'),
    # Поиск новых участников на странице приглашения
    path('invites/search/', team_views.search_new_teammates, name='search_new_teammate'),
    # Вступить в команду по ссылке
    path('invite_team/<str:key>/', team_views.join_using_link, name='join_using_link'),
    # Пригласить пользователя
    path('invites/invite/<int:profile_id>', team_views.join_user_from_page, name='join_user_from_page'),
    # Выгнать пользователя из команды
    path('leave/', team_views.kick_teammate, name='kick_teammate'),
    # Присоединиться через уведомление
    path('invite/', team_views.join_from_notification, name='join_from_notification'),
    # Создание нового опроса через команду
    path('create_poll/', team_views.redirect_create_poll, name='create_poll_from_team')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
