import django.urls

from main.views import user_views

urlpatterns = [
    # Регистрация
    django.urls.path('', user_views.user_register, name='register'),
    # Отправка кода подтверждения
    django.urls.path('register/send_email', user_views.send_email),
    # Проверка кода
    django.urls.path('register/complete', user_views.check_verification_code),
]
