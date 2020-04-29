from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import profile_views, user_views, teams_views, company_views, poll_views, questions_views, \
    auxiliary_general_methods

app_name = "main"
urlpatterns = [
                  # Регистрация
                  path('register/', user_views.user_register, name='register'),
                  # Начальная страница
                  path('', user_views.user_login, name='login'),
                  # Выход
                  path('logout/', user_views.user_logout, name='logout'),

                  # Сообщение об успешной смене пароля
                  path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
                      template_name='main/registration/password_change_done.html'),
                       name='password_change_done'),
                  # Изменение пароля
                  path('password_change/',
                       auth_views.PasswordChangeView.as_view(template_name='main/registration/password_change.html',
                                                             success_url=reverse_lazy('main:password_change_done')),
                       name='password_change'),
                  # Сообщение об отправке сообщения на почту
                  path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='main/registration/password_reset_done.html'),
                       name='password_reset_done'),
                  # Неведомая и странно работающая часть
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                      template_name='main/registration/password_reset_confirm.html',
                      success_url=reverse_lazy('main:password_reset_complete')
                  ),
                       name='password_reset_confirm'),
                  # Сброс пароля
                  path('password_reset/', auth_views.PasswordResetView.as_view(
                      template_name='main/registration/password_reset_form.html',
                      subject_template_name='main/registration/password_reset_subject.txt',
                      email_template_name='main/registration/password_reset_email.html',
                      success_url=reverse_lazy('main:password_reset_done')),
                       name='password_reset'),
                  # Сообщение об успешном сбросе пароля
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='main/registration/password_reset_complete.html'),
                       name='password_reset_complete'),

                  # Просмотр профиля
                  path('<int:profile_id>/', profile_views.profile_view, name='profile'),
                  # Редактирование профиля
                  path('edit/', profile_views.edit_profile, name='edit'),
                  # Загрузка аватарки
                  path('upload_photo/', profile_views.upload_profile_photo, name='upload_photo'),
                  # Просмотр других пользователей
                  # path('other_user/<int:profile_id>/', profile_views.other_profile_view, name='other_user_view'),
                  # Поиск пользователей
                  path('search_profile/', auxiliary_general_methods.find_user, name='search_profile'),

                  # Обзор коммуникаций юзера
                  path('communications/', teams_views.teams_view, name='communications'),
                  # Промотр конкретной команды
                  path('groups/<int:group_id>/', teams_views.team_user_view, name='group_user_view'),
                  # Создание группы команды
                  path('create_group/', teams_views.create_team, name='create_group'),
                  # Присоединение к команде (по ключу)
                  path('connect_to_group/', teams_views.connect_to_team_to_key, name='connect_to_group'),
                  # Присоединение к команде (по ссылке)
                  path('invite/t/<str:key>/', teams_views.connect_to_team_to_link, name='connect_to_team_to_link'),

                  # Создание компании (для ясности стоит изменить url)
                  path('add_company/', company_views.create_company, name='add_company'),
                  # Просмотр компании (список должностей и платформ, название компании,
                  #     ее владелец и ключ для присоединения)
                  path('company_view/', company_views.company_view, name='company_view'),
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
                  path('search_hr/', company_views.search_hr, name='search_hr_and_redirect_to_add_method'),
                  path('add_hr/<int:profile_id', company_views.add_hr, name='add_hr_method'),

                  # Поиск вопроса среди имеющихся
                  path('questions_search/', questions_views.find_question, name='questions_search'),
                  # Добавление нового вопроса
                  path('add_new_question', questions_views.add_new_question, name="add_new_question"),

                  # Создание опроса
                  path('create_poll/', poll_views.create_pool, name='create_pool'),
                  # Добавление вопросов к опросу
                  path('<int:pool_id>/add_question', poll_views.add_questions_in_poll, name='add_question_in_pool'),
                  # Добавление ответа к вопросу опроса
                  path('<int:poll_id>/add_answer/<int:question_id>/', poll_views.add_answer,
                       name='add_answer_in_poll_for_question'),
                  # Возвращает список вопросов
                  path('<int:poll_id>/poll_questions/', poll_views.questions_in_pool_view,
                       name='view_questions_in_poll'),
                  #
                  path('default_poll_view/', poll_views.default_poll_template_view, name='default_poll_view'),

                  # Ответ на опрос
                  path('poll', poll_views.answer_the_poll, name='answer_the_poll'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
