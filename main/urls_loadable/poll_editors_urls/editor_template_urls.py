from django.urls import path

from ...views.poll_views import create_poll_from_template

urlpatterns = [
    # Создание нового опроса через шаблон
    path('', create_poll_from_template.create_poll_from_template,
         name='create_poll_from_template'),
    # Сохранение шаблона
    path('save_as/', create_poll_from_template.save_template, name='save_template'),
    # Переход с первого на второй шаг
    path('step/2/from/1/',
         create_poll_from_template.render_step_2_from_step_1, name='choose_respondents'),
    # Загрузка команд на втором шаге
    path('step/2/category/teams/',
         create_poll_from_template.render_category_teams_on_step_2),
    # Загрузка участников компании на втором шаге
    path('step/2/category/participants/',
         create_poll_from_template.render_category_participants_on_step_2),
    # Поиск на втором шаге
    path('step/2/search/', create_poll_from_template.search_step_2),
    # Переход на первый шаг со второго
    path('step/1/from/2/', create_poll_from_template.render_step_1_from_step_2),
    # Переход на первый шаг с третьего
    path('step/1/from/3/', create_poll_from_template.render_step_1_from_step_3),
    # Переход на третий шаг с первого
    path('step/3/from/1/', create_poll_from_template.render_step_3_from_step_1),
    # Переход на третий шаг со второго
    path('step/3/from/2/', create_poll_from_template.render_step_3_from_step_2),
    # Переход на третий шаг со второго
    path('step/2/from/3/', create_poll_from_template.render_step_2_from_step_3),
    # Переход на третий шаг для не мастера (второй шаг для пользователя)
    path('step/3/from/1/notMaster/',
         create_poll_from_template.render_step_3_from_step_1_not_master),
    # Перехо на первый шаг с третьего для не мастера (на первый со второго для пользователя)
    path('step/1/from/3/notMaster/',
         create_poll_from_template.render_step_1_from_step_3_not_master),
    # Загрузка команд на третьем шаге
    path('step/3/category/teams/',
         create_poll_from_template.render_category_teams_on_step_3),
    # Загрузка участников компании на третьем шаге
    path('step/3/category/participants/',
         create_poll_from_template.render_category_participants_on_step_3),
    # Поиск на третьем шаге
    path('step/3/search/', create_poll_from_template.search_step_3),
    # Превьюшка для опроса
    path('step/1/category/preview/', create_poll_from_template.poll_preview),
    # Возврат к редактированию опроса
    path('step/1/category/editor/', create_poll_from_template.poll_editor),
    # Отмена создания опроса
    path('cancel/', create_poll_from_template.cancel_created_poll),
    # Отправить опросы опрашиваемым и разослать уведомления на почту
    path('send/', create_poll_from_template.send_poll),
]
