from django.urls import path

from ..views import teams_views

urlpatterns = [
    # Список всх команд
    path('', teams_views.teams_view, name='teams_view'),
    # Приглашение новых участников через команду
    path('<int:team_id>/invites', teams_views.team_new_invites, name='team_new_invites'),
    # Создание команды
    path('create_team/', teams_views.create_team, name='create_team'),
]
