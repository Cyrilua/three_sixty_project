from .poll_urls import editor
from django.urls import path, include

urlpatterns = [
    path('editor/', include(editor))
]
