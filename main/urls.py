from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import profile_views, user_views, teams_views, company_views, poll_views_old, \
    auxiliary_general_methods, notifications_views, test
from .views.poll_views import create_poll, polls_view, result_poll, create_poll_from_template, compiling_poll
from .views.profile_views import render_profile, edit_profile

app_name = "main"
urlpatterns = [
                  # Регистрация
                  path('register/', user_views.user_register, name='register'),
                  # Отправка кода подтверждения
                  path('register/register/send_email', user_views.send_email),
                  # Проверка кода
                  path('register/register/complete', user_views.check_verification_code),
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
                  path('edit/', edit_profile.edit_profile, name='edit'),
                  # Удаление платформы из профиля
                  path('edit/platform/remove/<int:platform_id>', edit_profile.remove_platform),
                  # Удаление должности из профиля
                  path('edit/position/remove/<int:position_id>', edit_profile.remove_position),
                  # Добавление платформы
                  path('edit/platform/add/<int:platform_id>', edit_profile.add_platform),
                  # Добавление должности
                  path('edit/position/add/<int:position_id>', edit_profile.add_position),
                  # Проверка имени
                  path('edit/check_input/name', edit_profile.check_name),
                  # Проверка фамилии
                  path('edit/check_input/surname', edit_profile.check_surname),
                  # Проверка отчества
                  path('edit/check_input/patronymic', edit_profile.check_patronymic),
                  # Сохранение ФИО
                  path('edit/edit/save/name', edit_profile.save_changes_fcs),
                  # Проверка даты
                  path('edit/check_input/birthdate', edit_profile.check_birth_date),
                  # Сохранение даты
                  path('edit/edit/save/birthdate', edit_profile.save_birth_date),
                  # Проверка корректности ввода почты
                  path('edit/check_input/email', edit_profile.check_email),
                  # Сохранение новой почты
                  path('edit/edit/save/email', edit_profile.save_email),
                  # Oтправка сообщения с подтверждением
                  path('edit/edit/save/email/send_mail', edit_profile.send_email_verification_code),
                  # Проверка кода из письма
                  path('edit/edit/save/email_code', edit_profile.check_email_code),
                  # Проверка логина
                  path('edit/check_input/username', edit_profile.check_login),
                  # Сохранение логина
                  path('edit/edit/save/username', edit_profile.save_login),
                  # Проверка нового пароля 1
                  path('edit/check_input/password1', edit_profile.check_new_password_1),
                  # Проверка нового пароля 2
                  path('edit/check_input/password2', edit_profile.check_new_password_2),
                  # Сохранение нового пароля
                  path('edit/edit/save/password', edit_profile.save_new_password),
                  # Загрузка аватарки
                  path('edit/edit/photo/update', edit_profile.upload_profile_photo),
                  # Удаление аватарки
                  path('edit/edit/photo/delete', edit_profile.delete_profile_photo),

                  # Промотр конкретной команды
                  path('team/<int:group_id>/', teams_views.team_user_view, name='group_user_view'),
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

                  # Создание компании (для ясности стоит изменить url)
                  path('add_company/', company_views.create_company, name='add_company'),
                  # Просмотр компании (список должностей и платформ, название компании,
                  #     ее владелец и ключ для присоединения)
                  path('company_view/<int:id_company>/', company_views.company_view, name='company_view'),
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
                  # Поиск пользователя для назначения его админом
                  path('search_admin/', company_views.search_admins, name='search_admins_and_redirect_to_add_method'),
                  # Контроллер, на который ссылается поиск админа
                  path('add_admin/<int:profile_id>', company_views.add_admins, name='add_admin_method'),
                  # Поиск пользователя для назначения его HR
                  path('search_hr/', company_views.search_hr, name='search_hr_and_redirect_to_add_method'),
                  # Контроллер, на который ссылается поиск HR
                  path('add_hr/<int:profile_id>', company_views.add_hr, name='add_hr_method'),

                  # Выполнение уведомления
                  path('notifications/<int:notification_id>/', notifications_views.redirect_from_notification),

                  ########## New poll ######################
                  # Страница просмотра опросов и шаблонов
                  path('polls/', polls_view.polls_view, name='new_poll_view'),
                  #
                  path('poll/editor/', create_poll_from_template.create_poll_from_template, name='poll_editor_id'),
                  #
                  path('poll/editor/new/', create_poll.poll_create_redirect, name='poll_editor'),
                  # Просмотр результата опроса
                  path('poll/result/<int:poll_id>/', result_poll.result_poll, name='poll_result'),
                  # Динамическая подгрузка опросов
                  path('polls/loading/<int:count_polls>/', polls_view.loading_polls),
                  # Маячок о новом опросе для прохождения
                  path('polls/new_notif/', polls_view.load_notification_new_poll),
                  # Создание нового опроса через шаблон
                  path('poll/editor/template/<int:template_id>/', create_poll_from_template.create_poll_from_template,
                       name='create_poll_from_template'),
                  # Сохранение шаблона
                  path('poll/editor/template/<int:template_id>/save_as/', create_poll_from_template.save_template,
                       name='save_template'),
                  # Переход с первого на второй шаг
                  path('poll/editor/template/<int:template_id>/step/2/from/1/',
                       create_poll_from_template.render_step_2_from_step_1, name='choose_respondents'),
                  # Загрузка команд на втором шаге
                  path('poll/editor/template/<int:template_id>/step/2/category/teams/',
                       create_poll_from_template.render_category_teams_on_step_2),
                  # Загрузка участников компании на втором шаге
                  path('poll/editor/template/<int:template_id>/step/2/category/participants/',
                       create_poll_from_template.render_category_participants_on_step_2),
                  # Поиск на втором шаге
                  path('poll/editor/template/<int:template_id>/step/2/search/',
                       create_poll_from_template.search_step_2),
                  # Переход на первый шаг со второго
                  path('poll/editor/template/<int:template_id>/step/1/from/2/',
                       create_poll_from_template.render_step_1_from_step_2),
                  # Переход на первый шаг с третьего
                  path('poll/editor/template/<int:template_id>/step/1/from/3/',
                       create_poll_from_template.render_step_1_from_step_3),
                  # Переход на третий шаг с первого
                  path('poll/editor/template/<int:template_id>/step/3/from/1/',
                       create_poll_from_template.render_step_3_from_step_1),
                  # Переход на третий шаг со второго
                  path('poll/editor/template/<int:template_id>/step/3/from/2/',
                       create_poll_from_template.render_step_3_from_step_2),
                  # Переход на третий шаг со второго
                  path('poll/editor/template/<int:template_id>/step/2/from/3/',
                       create_poll_from_template.render_step_2_from_step_3),
                  # Переход на третий шаг для не мастера (второй шаг для пользователя)
                  path('poll/editor/template/<int:template_id>/step/3/from/1/notMaster/',
                       create_poll_from_template.render_step_3_from_step_1),
                  # Перехо на первый шаг с третьего для не мастера (на первый со второго для пользователя)
                  path('poll/editor/template/<int:template_id>/step/1/from/3/notMaster/',
                       create_poll_from_template.render_step_1_from_step_3),
                  # Загрузка команд на третьем шаге
                  path('poll/editor/template/<int:template_id>/step/3/category/teams/',
                       create_poll_from_template.render_category_teams_on_step_3),
                  # Загрузка участников компании на третьем шаге
                  path('poll/editor/template/<int:template_id>/step/3/category/participants/',
                       create_poll_from_template.render_category_participants_on_step_3),
                  # Поиск на третьем шаге
                  path('poll/editor/template/<int:template_id>/step/3/search/',
                       create_poll_from_template.search_step_3),
                  # Превьюшка для опроса
                  path('poll/editor/template/<int:template_id>/step/1/category/preview/',
                       create_poll_from_template.poll_preview),
                  # Возврат к редактированию опроса
                  path('poll/editor/template/<int:template_id>/step/1/category/editor/',
                       create_poll_from_template.poll_editor),
                  # Отмена создания опроса
                  path('poll/editor/template/<int:template_id>/cancel/',
                       create_poll_from_template.cancel_created_poll),
                  # Отправить опросы опрашиваемым и разослать уведомления на почту
                  path('poll/editor/template/<int:template_id>/send/',
                       create_poll_from_template.send_poll),
                  # Удаление шаблона
                  path('polls/template/remove/', polls_view.remove_template),
                  # Отметить опрос опросмотренным
                  path('polls/viewing/<int:poll_id>', polls_view.mark_as_viewed),
                  #
                  path('compiling_poll/<int:poll_id>/', compiling_poll.compiling_poll, name='compiling_poll'),

                  ############ Only for debug ###############
                  path('test/', test.test)

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
