from django.urls import path

from ..views.teams import teams_views

urlpatterns = [
    # Список всх команд
    path('', teams_views.teams_view, name='teams_view'),
    # Создание команды
    path('create_team/', teams_views.create_team, name='create_team'),
    # Поиск по командам
    path('search/', teams_views.search_teams, name='search')
]
