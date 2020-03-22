from django.urls import path
from . import views


app_name = "main"
urlpatterns = [
    path('user/', views.user_view),
    path('', views.index_view, name='index'),
    path('login/', views.user_login, name='login'),
    path('groups/', views.groups_view, name='groups'),
    path('register/', views.user_register, name='register')

]
