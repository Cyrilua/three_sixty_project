from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import profile_views, user_views, teams_views, company_views, poll_views, questions_views

app_name = "main"
urlpatterns = [
    path('register/', user_views.user_register, name='register'),
    path('', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),

    path('profile/', profile_views.user_view, name='profile'),
    path('edit/', profile_views.edit_profile, name='edit'),
    path('upload_photo/', profile_views.upload_profile_photo, name='upload_photo'),
    path('other_user/<int:profile_id>/', profile_views.other_profile_view, name='other_user_view'),

    path('communications/', teams_views.teams_view, name='communications'),
    path('groups/<int:group_id>/', teams_views.team_user_view, name='group_user_view'),
    path('create_group/', teams_views.create_team, name='create_group'),
    path('connect_to_group/', teams_views.connect_to_team, name='connect_to_group'),
    path('connect_to_group/', teams_views.connect_to_team, name='connect_to_group'),

    path('add_company/', company_views.add_company, name='add_company'),
    path('company_view/', company_views.company_view, name='company_view'),
    path('connect_to_company/', company_views.connect_to_company, name='connect_to_company'),
    path('get_all_companies_users/', company_views.get_all_users_in_company, name='get_all_companies_users'),
    path('add_new_platform/', company_views.add_new_platform, name='add_new_platform'),
    path('add_new_position/', company_views.add_new_position, name='add_new_position'),
    path('add_new_position_in_company/', company_views.add_position_in_company, name="add_new_position_in_company"),
    path('add_new_platform_in_company/', company_views.add_platform_in_company, name="add_new_platform_in_company"),
    path('get_all_positions/', company_views.all_positions_in_company_views, name="all_positions_in_company"),
    path('choose_position/<int:position_id>/', company_views.choose_position, name='choose_position_in_company'),

    path('questions_search/', questions_views.find_question, name='questions_search'),
    path('add_new_question', questions_views.add_new_question, name="add_new_question"),

    path('create_poll/', poll_views.create_pool, name='create_pool'),
    path('<int:pool_id>/add_question', poll_views.add_questions_in_poll, name='add_question_in_pool'),
    path('<int:poll_id>/add_answer/<int:question_id>/', poll_views.add_answer, name='add_answer_in_poll_for_question'),
    path('<int:poll_id>/poll_questions/', poll_views.questions_in_pool_view, name='view_questions_in_poll'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
