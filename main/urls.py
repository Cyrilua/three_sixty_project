from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


app_name = "main"
urlpatterns = [
    path('profile/', views.user_view, name='profile'),
    path('', views.user_login, name='login'),
    # path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('communications/', views.teams_view, name='communications'),
    path('groups/<int:group_id>/', views.team_user_view, name='group_user_view'),
    path('register/', views.user_register, name='register'),
    path('edit/', views.edit_profile, name='edit'),
    path('company_view/', views.company_view, name='company_view'),
    path('upload_photo/', views.upload_profile_photo, name='upload_photo'),

    path('other_user/<int:profile_id>/', views.other_user_view, name='other_user_view'),
    path('add_company/', views.add_company, name='add_company'),
    path('connect_to_company/', views.connect_to_company, name='connect_to_company'),
    path('get_all_companies_users/', views.get_all_users_in_company, name='get_all_companies_users'),
    path('add_new_platform/', views.add_new_platform, name='add_new_platform'),
    path('add_new_position/', views.add_new_position, name='add_new_position'),
    path('add_new_position_in_company/', views.add_position_in_company, name="add_new_position_in_company"),
    path('add_new_platform_in_company/', views.add_platform_in_company, name="add_new_platform_in_company"),
    path('create_group/', views.create_team, name='create_group'),
    path('connect_to_group/', views.connect_to_team, name='connect_to_group'),
    path('questions_search/', views.find_question, name='questions_search'),
    path('create_poll/', views.create_pool, name='create_pool'),
    #path('view_poll/<int:id_pool>/', views.poll_view, name='view_poll'),
    path('<int:pool_id>/add_question', views.add_questions_in_poll, name='add_question_in_pool'),
    path('add_new_question', views.add_new_question, name="add_new_question"),
    path('<int:poll_id>/add_answer/<int:question_id>/', views.add_answer, name='add_answer_in_poll_for_question'),
    path('<int:poll_id>/poll_questions/', views.questions_in_pool_view, name='view_questions_in_poll'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
