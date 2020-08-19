from .poll_editors_urls import editor_template_urls, editor_new_poll_urls
from django.urls import path, include

urlpatterns = [
    # Создание опроса из шаблона
    path('editor/template/<int:template_id>/', include(editor_template_urls)),
    # Создание нового опроса
    path('editor/new/', include(editor_new_poll_urls))
]
