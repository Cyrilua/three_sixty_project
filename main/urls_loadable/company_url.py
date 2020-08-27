from django.urls import path

from ..views import company_views

urlpatterns = [
    # Просмотр компании
    path('', company_views.company_view, name='company_view'),
    # Настроки команды
    path('setting/', company_views.company_setting, name='company_setting'),
    # Добавить позицию
    path('setting/position/add/', company_views.add_position),
    # Удалить позицию
    path('setting/position/<int:position_id>/remove/', company_views.remove_position),
    # Добавить платформу
    path('setting/platform/add/', company_views.add_platform),
    # Удалить платформу
    path('setting/platform/<int:platform_id>/remove/', company_views.remove_platform),
    # Сохранить изенения
    path('setting/change/', company_views.save_settings_change),
    # Загрузка команд
    path('load/', company_views.load_teams_and_users),
    # Удаление команды
    path('team/<int:team_id>/remove/', company_views.remove_team),
    #
    #path('create_new_poll_from_company/<int:company_id>/', )
]
