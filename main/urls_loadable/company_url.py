from django.urls import path

from ..views import company_views

urlpatterns = [
    # Просмотр компании
    path('', company_views.company_view, name='company_view'),
    # Настроки команды
    path('setting/', company_views.company_setting, name='company_setting'),
    # Добавить позицию
    path('setting/position/add/', company_views.add_position),
    # Загрузка команд
    path('load/', company_views.load_teams_and_users),
    # Удаление команды
    path('team/<int:team_id>/remove/', company_views.remove_team)
]
