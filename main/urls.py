from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.user_view, name='user'),
    path('', views.index_view, name='index'),
]
