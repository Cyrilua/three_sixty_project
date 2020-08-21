from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import profile_views, user_views, teams_views, company_views, poll_views_old, \
    auxiliary_general_methods, test
from .views.poll_views import create_poll, polls_view, result_poll, create_poll_from_template, compiling_poll
from .views.profile_views import render_profile, edit_profile
from main import urls_loadable
from .urls_loadable import register_urls, edit_profile_urls, polls_view_urls, poll_urls

app_name = "main"
urlpatterns = [
                  # Регистрация
                  path('register/', include(register_urls)),
                  # Начальная страница
                  path('', user_views.user_login, name='login'),
                  # Выход
                  path('logout/', user_views.user_logout, name='logout'),

                  # Сообщение об успешной смене пароля
                  path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
                      template_name='main/password/password_change_done.html'),
                       name='password_change_done'),
                  # Изменение пароля
                  path('password_change/',
                       auth_views.PasswordChangeView.as_view(template_name='main/password/password_change.html',
                                                             success_url=reverse_lazy('main:password_change_done')),
                       name='password_change'),
                  # Сообщение об отправке сообщения на почту
                  path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='main/password/password_reset_done.html'),
                       name='password_reset_done'),
                  # Неведомая и странно работающая часть
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                      template_name='main/password/password_reset_confirm.html',
                      success_url=reverse_lazy('main:login')
                  ),
                       name='password_reset_confirm'),
                  # Сброс пароля
                  path('password_reset/', auth_views.PasswordResetView.as_view(
                      template_name='main/password/password_reset_form.html',
                      subject_template_name='main/password/password_reset_subject.txt',
                      email_template_name='main/password/password_reset_email.html',
                      success_url=reverse_lazy('main:password_reset_done')),
                       name='password_reset'),
                  # Сообщение об успешном сбросе пароля
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='main/password/old/password_reset_complete.html'),
                       name='password_reset_complete'),

                  # Просмотр профиля
                  path('<int:profile_id>/', render_profile.profile_view, name='profile'),
                  # Редактирование профиля
                  path('edit/', include(edit_profile_urls), name='edit'),

                  # Промотр конкретной команды
                  path('team/<int:group_id>/', teams_views.team_user_view, name='team_view'),
                  # Создание команды
                  path('create_team/', teams_views.create_team, name='create_team'),
                  # Присоединение к команде (по ключу)
                  path('connect_to_command/', teams_views.connect_to_team_to_key, name='connect_to_group'),
                  # Присоединение к команде (по ссылке)
                  path('invite/t/<str:key>/', teams_views.connect_to_team_to_link, name='connect_to_team_to_link'),
                  # Поиск команды для присоединения в нее
                  path('<int:profile_id>/invite/', teams_views.search_team_for_invite, name='search_team_for_invite'),
                  # Отправить уведомление о приглашении
                  path('<int:profile_id>/invite/<int:team_id>/', teams_views.send_notification_profile),

                  # Список всх команд
                  path('teams/', teams_views.teams_view, name='teams_view'),
                  # Настройки команды
                  path('team/<int:team_id>/setting', teams_views.team_setting, name='team_setting'),
                  # Приглашение новых участников через команду
                  path('team/<int:team_id>/invites', teams_views.team_new_invites, name='team_new_invites'),

                  # Создание компании (для ясности стоит изменить url)
                  path('add_company/', company_views.create_company, name='add_company'),
                  # Просмотр компании (список должностей и платформ, название компании,
                  #     ее владелец и ключ для присоединения)
                  path('company/<int:id_company>/', company_views.company_view, name='company_view'),
                  # Настроки команды
                  path('company/<int:id_company>/setting/', company_views.company_setting, name='company_setting'),
                  # Присоединение к компании (по ключу)
                  path('connect_to_company/', company_views.connect_to_company_to_key, name='connect_to_company'),
                  # Присоеддинение к компании (по ссылке)
                  path('invite/c/<str:key>/', company_views.connect_to_company_to_link,
                       name="connect_to_company_to_link"),
                  # Возвращает список пользователей в компани
                  path('get_all_companies_users/', company_views.get_all_users_in_company,
                       name='get_all_companies_users'),
                  # Добавление новой платформы (может сделать человек, не состоящий в компании)
                  path('add_new_platform/', company_views.add_new_platform, name='add_new_platform'),
                  # Добавление новой должности (может сделать человек, не состоящий в компании)
                  path('add_new_position/', company_views.add_new_position, name='add_new_position'),
                  # Добавление новой должности в компанию (если должности не существует - она будет создана)
                  path('add_new_position_in_company/', company_views.add_position_in_company,
                       name="add_new_position_in_company"),
                  # Добавление новой платформы в компанию (если платформы не существует - она будет создана)
                  path('add_new_platform_in_company/', company_views.add_platform_in_company,
                       name="add_new_platform_in_company"),
                  # Сохраняет конкретную должность для пользователя
                  path('choose_position/', company_views.choose_position,
                       name='position_choice'),
                  # Сохраняет конкретную платформу для пользователя
                  path('choose_platform/', company_views.choose_platform,
                       name="platform_choice"),

                  ########## New poll ######################
                  # Страница просмотра опросов и шаблонов
                  path('polls/', include(polls_view_urls), name='new_poll_view'),
                  # Создание нового опроса через шаблон
                  path('poll/', include(poll_urls), name='poll'),

                  ############ Only for debug ###############
                  path('test/', test.test)

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
