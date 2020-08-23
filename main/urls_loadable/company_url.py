from django.urls import path

from ..views import company_views

urlpatterns = [
    # Просмотр компании
    path('<int:id_company>/', company_views.company_view, name='company_view'),
    # Настроки команды
    path('<int:id_company>/setting/', company_views.company_setting, name='company_setting'),
]
