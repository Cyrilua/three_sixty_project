from django.urls import path

from ..views.profile_views import render_profile

urlpatterns = [
    # Просмотр профиля
    path('', render_profile.profile_view, name='profile'),
    path('loading', render_profile.loading, name='loading'),
]
