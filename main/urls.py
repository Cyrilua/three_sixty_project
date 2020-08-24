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
from .urls_loadable import register_urls, edit_profile_urls, polls_view_urls, poll_urls, company_url,\
teams_views_urls, team_urls

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

    # Страница команд
    path('teams/', include(teams_views_urls), name='teams_view'),
    # Промотр конкретной команды
    path('team/', include(team_urls), name='team_view'),
    # Поиск команды для присоединения в нее
    path('<int:profile_id>/invite/', teams_views.search_team_for_invite, name='search_team_for_invite'),


    # Страница просмотра опросов и шаблонов
    path('polls/', include(polls_view_urls), name='new_poll_view'),
    # Создание нового
    path('poll/', include(poll_urls), name='poll'),
    # Страница компании
    path('company/<int:id_company>/', include(company_url), name='company_view'),


    ############ Only for debug ###############
    path('test/', test.test),
    # Создание компании (для ясности стоит изменить url)
    path('add_company/', company_views.create_company, name='add_company'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
