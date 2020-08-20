from datetime import datetime

from main.views.auxiliary_general_methods import *
from main.models import Poll, TemplatesPoll, Questions, Settings, Group, Moderator, SurveyWizard, Company,\
    AnswerChoice, NeedPassPoll
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.template.response import SimpleTemplateResponse
from .create_poll_views.start_create import build_questions


def compiling_poll(request: WSGIRequest, poll_id: int) -> render:
    if request.method == "GET":
        try:
            poll = Poll.objects.get(id=poll_id)
        except ObjectDoesNotExist:
            return render(request, 'main/errors/global_error.html', {'global_error': '404'})

        profile = get_user_profile(request)
        if not NeedPassPoll.objects.filter(poll=poll, profile=profile).exists():
            return render(request, 'main/errors/global_error.html', {'global_error': '403'})
        collected_poll = _build_poll_compiling(poll)
        return render(request, 'main/poll/taking_poll.html', {'poll': collected_poll})


def _build_poll_compiling(poll: Poll):
    return {
        'color': poll.color,
        'is_not_preview': True,
        'name': poll.name_poll,
        'target': {
            'href': '/{}/'.format(poll.target.pk),
            'name': poll.target.name,
            'surname': poll.target.surname,
            'patronymic': poll.target.patronymic
        },
        'description': poll.description,
        'questions': build_questions(poll.questions.all(), False)
    }


def compiling_poll_link(request: WSGIRequest, poll_key: int) -> render:
    # todo
    return render(request, 'main/poll/taking_poll.html', {})
