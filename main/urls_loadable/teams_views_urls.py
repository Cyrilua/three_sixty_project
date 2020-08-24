from django.urls import path

from ..views import teams_views

urlpatterns = [
    # Список всх команд
    path('', teams_views.teams_view, name='teams_view'),
    # Настройки команды
    path('<int:team_id>/setting', teams_views.team_setting, name='team_setting'),
    # Приглашение новых участников через команду
    path('<int:team_id>/invites', teams_views.team_new_invites, name='team_new_invites'),
]