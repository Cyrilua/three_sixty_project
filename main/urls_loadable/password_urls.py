from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy

urlpatterns = [
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
        email_template_name='main/email/email.html',
        html_email_template_name='main/email/email.html',
        success_url=reverse_lazy('main:password_reset_done')),
         name='password_reset'),
    # Сообщение об успешном сбросе пароля
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='main/password/old/password_reset_complete.html'),
         name='password_reset_complete'),

]
