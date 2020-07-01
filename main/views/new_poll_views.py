import uuid

from main.models import Questions, Poll, Answers, CompanyHR, AnswerChoice, Settings, TextAnswer, TemplatesPoll, Group, \
    NeedPassPoll, CreatedPoll
from main.views.auxiliary_general_methods import *
from main.views.notifications_views import add_notification
from django.views.generic import View
from django.http import JsonResponse
from django.template import loader


class CreatePoll(View):
    def get(self, request):
        pageContainer = loader.render_to_string('main/poll/polll_editor.html')
        rightMenu = loader.render_to_string('main/includes/menu_poll_editor_right.html')
        data = {
            'pageContainer': pageContainer,
            'rightMenu': rightMenu
        }
        return JsonResponse(data, status=200)
