from django.urls import path

from ..views.poll_views import create_poll, polls_view

urlpatterns = [
    # Страница просмотра опросов и шаблонов
    path('', polls_view.polls_view, name='new_poll_view'),
    # Динамическая подгрузка опросов
    path('loading/<int:count_polls>/', polls_view.loading_polls),
    # Маячок о новом опросе для прохождения
    path('new_notif/', polls_view.load_notification_new_poll),
    # Создание нового опроса todo
    path('poll/create/', create_poll.redirect_for_create, name='poll_create'),
    # Удаление шаблона
    path('template/remove/', polls_view.remove_template),
    # Отметить опрос опросмотренным
    path('viewing/<int:poll_id>', polls_view.mark_as_viewed),
]
