from django.urls import path

from ..views import company_views


urlpatterns = [
    # Просмотр компании
    path('', company_views.company_view, name='company_view'),
    # Создать опрос
    path('create_poll/', company_views.redirect_create_poll, name='create_poll_from_company'),
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
    # Получить ссылку для присоединения в компанию
    path('setting/get_link_invite/', company_views.get_invite_link),
    # Загрузка команд
    path('load/', company_views.load_teams_and_users),
    # Удаление команды
    path('team/<int:team_id>/remove/', company_views.remove_team),
    # Добавить роль пользователю
    path('user/<int:profile_id>/edit/role/add/', company_views.assign_role_profile, name='assign_role_profile'),
    # Удалить роль пользователю
    path('user/<int:profile_id>/edit/role/remove/', company_views.remove_role_from_profile),
    # Добавить должность пользователю
    path('user/<int:profile_id>/edit/position/<int:position_id>/add/', company_views.assign_position_profile),
    # Добавить платформу пользователю
    path('user/<int:profile_id>/edit/platform/<int:platform_id>/add/', company_views.assign_platform_profile),
    # Удалить должность пользователю
    path('user/<int:profile_id>/edit/position/<int:position_id>/remove/', company_views.remove_position_profile),
    # Удалить должность пользователю
    path('user/<int:profile_id>/edit/platform/<int:platform_id>/remove/', company_views.remove_platform_profile),

    # Кикнуть пользователя
    path('user/<int:profile_id>/dismiss/', company_views.kick_profile_from_company),
    # Присоединиться по ссылке
    path('invite_company/<str:key>/', company_views.join_company_from_link, name='join_company_from_link'),
]
