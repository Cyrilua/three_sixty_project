from django.urls import path
from . import views


app_name = "main"
urlpatterns = [
    path('user/', views.user_view, name='user'),
    path('', views.user_login, name='login'),
    # path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('communications/', views.team_view, name='groups'),
    path('groups/<int:group_id>/', views.team_user_view, name='group_user_view'),
    path('register/', views.user_register, name='register'),
    path('other_user/<int:profile_id>/', views.other_user_view, name='other_user_view'),

    path('change_profile_test/', views.change_user_profile, name='change_profile'),
    path('add_company_test/', views.add_company, name='add_company'),
    path('connect_to_company_test/', views.connect_to_company, name='connect_to_company'),
    path('get_all_companies_users/', views.get_all_users_in_company, name='get_all_companies_users'),
    path('add_new_platform/', views.add_new_platform, name='add_new_platform'),
    path('add_new_position/', views.add_new_position, name='add_new_position'),
    path('create_group/', views.create_team, name='create_group'),
    path('connect_to_group/', views.connect_to_team, name='connect_to_group'),
    path('find_questions/', views.find_question, name='find_questions'),
    path('create_poll/', views.create_pool, name='create_pool'),
    path('view_poll/<int:id_pool>/', views.poll_view, name='view_poll'),
    path('create_poll/<int:pool_id>/add_question', views.add_questions_in_pool, name='add_question_in_pool')
]
