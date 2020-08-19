from django.urls import path


from ..views.profile_views import edit_profile

urlpatterns = [
    # Редактирование профиля
    path('', edit_profile.edit_profile, name='edit'),
    # Удаление платформы из профиля
    path('platform/remove/<int:platform_id>', edit_profile.remove_platform),
    # Удаление должности из профиля
    path('position/remove/<int:position_id>', edit_profile.remove_position),
    # Добавление платформы
    path('platform/add/<int:platform_id>', edit_profile.add_platform),
    # Добавление должности
    path('position/add/<int:position_id>', edit_profile.add_position),
    # Проверка имени
    path('check_input/name', edit_profile.check_name),
    # Проверка фамилии
    path('check_input/surname', edit_profile.check_surname),
    # Проверка отчества
    path('check_input/patronymic', edit_profile.check_patronymic),
    # Сохранение ФИО
    path('edit/save/name', edit_profile.save_changes_fcs),
    # Проверка даты
    path('check_input/birthdate', edit_profile.check_birth_date),
    # Сохранение даты
    path('edit/save/birthdate', edit_profile.save_birth_date),
    # Проверка корректности ввода почты
    path('check_input/email', edit_profile.check_email),
    # Сохранение новой почты
    path('edit/save/email', edit_profile.save_email),
    # Oтправка сообщения с подтверждением
    path('edit/save/email/send_mail', edit_profile.send_email_verification_code),
    # Проверка кода из письма
    path('edit/save/email_code', edit_profile.check_email_code),
    # Проверка логина
    path('check_input/username', edit_profile.check_login),
    # Сохранение логина
    path('edit/save/username', edit_profile.save_login),
    # Проверка нового пароля 1
    path('check_input/password1', edit_profile.check_new_password_1),
    # Проверка нового пароля 2
    path('check_input/password2', edit_profile.check_new_password_2),
    # Сохранение нового пароля
    path('edit/save/password', edit_profile.save_new_password),
    # Загрузка аватарки
    path('edit/photo/update', edit_profile.upload_profile_photo),
    # Удаление аватарки
    path('edit/photo/delete', edit_profile.delete_profile_photo),
]
