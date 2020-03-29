from django.urls import path
from . import views


app_name = "main"
urlpatterns = [
    path('user/', views.user_view, name='user'),
    path('', views.index_view, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('groups/', views.groups_view, name='groups'),
    path('register/', views.user_register, name='register'),

    path('user_test/', views.user_view_test, name='user_view_test'),
    path('add_company_test/', views.add_company_test, name='add_company_test'),
    path('connect_to_company_test/', views.connect_to_company, name='connect_to_company'),
    path('get_all_companies_users/', views.get_all_users_in_company, name='get_all_companies_users')
]
