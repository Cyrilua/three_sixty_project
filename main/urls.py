from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .urls_loadable import register_urls, edit_profile_urls, polls_view_urls, poll_urls, company_url, \
    teams_views_urls, team_urls, profile_urls, password_urls
from .views import user_views, company_views, test

app_name = "main"
urlpatterns = [
    # Регистрация
    path('register/', include(register_urls)),
    # Начальная страница
    path('', user_views.user_login, name='login'),
    # Выход
    path('logout/', user_views.user_logout, name='logout'),

    # Просмотр профиля
    path('<int:profile_id>/', include(profile_urls)),
    # Редактирование профиля
    path('edit/', include(edit_profile_urls)),

    # Страница команд
    path('teams/', include(teams_views_urls)),
    # Промотр конкретной команды
    path('team/<int:group_id>/', include(team_urls)),
    # Пригласить в команду с чужого профиля
    path('<int:profile_id>/invite/<int:group_id>/', teams_views_urls.teams_views.invite_to_team),
    # Отметить уведомления просмотренными
    path('<int:profile_id>/viewing/<int:notification_id>', profile_urls.render_profile.mark_notification_as_viewed),

    # Страница просмотра опросов и шаблонов
    path('polls/', include(polls_view_urls)),
    # Создание нового
    path('poll/', include(poll_urls)),
    # Страница компании
    path('company/<int:id_company>/', include(company_url)),

    ############ Only for debug ###############
    path('test/', test.test),
    # Создание компании (для ясности стоит изменить url)
    path('add_company/', company_views.create_company, name='add_company'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + password_urls.urlpatterns
