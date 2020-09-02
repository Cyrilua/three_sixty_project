from django.urls import path

from ..views.teams import teams_views

urlpatterns = [
    # Список всх команд
    path('', teams_views.teams_view, name='teams_view'),
    # Создание команды
    path('create_team/', teams_views.create_team, name='create_team'),
    # Поиск по командам
    path('search/', teams_views.search_teams, name='search'),
    # Список команд для приглашения со страницы чужого профиля
    path('invite/<int:profile_id>/', teams_views.team_for_invite, name='search_team_for_invite'),
    # Поиск по списку команд
    path('invite/<int:profile_id>/search/', teams_views.search_teams, name='search_team_for_invite'),
    # Пригласить в команду с чужого профиля
    path('invite/<int:profile_id>/send/', teams_views.invite_to_team)
]
