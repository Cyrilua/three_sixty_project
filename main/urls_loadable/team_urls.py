from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from ..views import profile_views, user_views, teams_views, company_views, poll_views_old, \
    auxiliary_general_methods, test
from ..views.poll_views import create_poll, polls_view, result_poll, create_poll_from_template, compiling_poll
from ..views.profile_views import render_profile, edit_profile
from main import urls_loadable
from ..urls_loadable import register_urls, edit_profile_urls, polls_view_urls, poll_urls, company_url, teams_views_urls

app_name = "main"
urlpatterns = [
    # Промотр конкретной команды
    path('<int:group_id>/', teams_views.team_view, name='team_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
