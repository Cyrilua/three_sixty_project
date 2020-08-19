from datetime import datetime

from main.views.auxiliary_general_methods import *
from main.models import Poll, TemplatesPoll, Questions, Settings, Group, Moderator, SurveyWizard, Company, AnswerChoice
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.template.response import SimpleTemplateResponse


def compiling_poll(request: WSGIRequest, poll_id: int) -> render:
    print('test')
    # todo
    return render(request, 'main/poll/taking_poll.html', {})


def compiling_poll_link(request: WSGIRequest, poll_key: int) -> render:
    # todo
    return render(request, 'main/poll/taking_poll.html', {})
