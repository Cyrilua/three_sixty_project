from . import editor_template_urls
from django.urls import path, include
from ..views.poll_views import result_poll, compiling_poll

urlpatterns = [
    # Создание опроса из шаблона
    path('editor/template/<int:template_id>/', include(editor_template_urls)),
    # Создание нового опроса
    path('editor/new/', include(editor_template_urls)),
    # Создание нового опроса через команду
    path('editor/team/<int:team_id>/new/', include(editor_template_urls)),
    # Создание нового опроса через компанию
    path('editor/company/<int:company_id>/new/', include(editor_template_urls)),
    # Просмотр результата опроса
    path('result/<int:poll_id>/', result_poll.result_poll, name='poll_result'),
    # Прохождение опроса (рендер)
    path('compiling_poll/<int:poll_id>/', compiling_poll.compiling_poll, name='compiling_poll_render'),
    # Прохождение опроса (отправка ответа)
    path('compiling_poll/<int:poll_id>/send/', compiling_poll.send_answer, name='compiling_poll_send'),
    # Прохождение опроса через ссылку
    path('compiling_poll_link/<str:poll_key>/', compiling_poll.compiling_poll_link,  name='compiling_poll_link'),
]
