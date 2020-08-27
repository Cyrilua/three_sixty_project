from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from ..views import profile_views, user_views, teams_views, company_views, poll_views_old, \
    auxiliary_general_methods, test
from ..views.poll_views import create_poll, polls_view, result_poll, create_poll_from_template, compiling_poll
from ..views.profile_views import render_profile, edit_profile
from main import urls_loadable
from ..urls_loadable import register_urls, edit_profile_urls, polls_view_urls, poll_urls, company_url, teams_views_urls

urlpatterns = [
    # Промотр конкретной команды
    path('', teams_views.team_view, name='team_view'),
    # Настройки команды
    path('settings/', teams_views.team_settings_view, name='team_setting'),
    # Удаление команды
    path('<settings/remove/', teams_views.team_remove, name='team_remove'),
    # Удаление команды
    path('settings/change/', teams_views.team_change, name='team_change'),
    # Поиск
    path('search/', teams_views.search_teammate, name='search'),
    # Приглашение новых участников через команду
    path('invites/', teams_views.team_new_invites, name='team_new_invites'),
    # Вступить в команду по ссылке
    path('invite_team/<str:key>/', teams_views.join_using_link, name='join_using_link'),
    # Пригласить пользователя
    path('invites/invite/<int:profile_id>', teams_views.join_user_from_page, name='join_user_from_page')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
