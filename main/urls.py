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

    path('change_profile_test/', views.change_user_profile_test, name='change_profile'),
    path('add_company_test/', views.add_company_test, name='add_company'),
    path('connect_to_company_test/', views.connect_to_company, name='connect_to_company'),
    path('get_all_companies_users/', views.get_all_users_in_company, name='get_all_companies_users'),
    path('add_new_platform/', views.add_new_platform, name='add_new_platform'),
    path('add_new_position/', views.add_new_position, name='add_new_position'),
    path('create_group/', views.create_group, name='create_group'),
    path('connect_to_group/', views.connect_to_group, name='connect_to_group'),
    path('find_questions/', views.find_question, name='find_questions')
]
