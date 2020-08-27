from main.views.auxiliary_general_methods import *
from main.models import SurveyWizard, Poll
from django.shortcuts import redirect, render
from django.http import JsonResponse
from . import create_poll_from_template
from django.core.handlers.wsgi import WSGIRequest


def redirect_for_create(request):
    if request.is_ajax():
        return JsonResponse({'urlNewPoll': '/poll/editor/new/'}, status=200)


def poll_create_from_team(request):
    # todo
    pass


def poll_create(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    args = {
        'title': "Создание опроса из шаблона",
        'poll': build_poll,
    }
    if SurveyWizard.objects.filter(profile=profile).exists():
        args['is_master'] = 'is_master'

    return render(request, 'main/poll/new_poll_editor.html', args)


def build_poll() -> dict:
    result = {
        'color': None,
        'questions': build_questions(),
    }
    return result


def build_questions() -> list:
    result = []
    collected_question = {
        'is_template': True,
        'type': 'checkbox',
        'countAnswers': 0,
    }
    result.append(collected_question)
    return result


def save_template(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.save_template(request, -1)


def render_category_teams_on_step_2(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_category_teams_on_step_2(request, -1)


def render_category_participants_on_step_2(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_category_participants_on_step_2(request, -1)


def search_step_2(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.search_step_2(request, -1)


def render_step_2_from_step_3(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_2_from_step_3(request, -1)


def render_step_1_from_step_3(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_1_from_step_3(request, -1)


def render_step_1_from_step_3_not_master(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    return render_step_1_from_step_3(request)


def render_step_3_from_step_2(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_3_from_step_2(request, -1)


def render_step_3_from_step_1(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_3_from_step_1(request, -1)


def render_step_3_from_step_1_not_master(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_3_from_step_1_not_master(request, -1)


def render_step_1_from_step_2(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_1_from_step_2(request, -1)


def render_step_2_from_step_1(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_2_from_step_1(request, -1)


def poll_preview(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.poll_preview(request, -1)


def poll_editor(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.poll_editor(request, -1)


def cancel_created_poll(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.cancel_created_poll(request, -1)


def send_poll(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.send_poll(request, -1)


def render_category_teams_on_step_3(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_category_teams_on_step_3(request, -1)


def render_category_participants_on_step_3(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_category_participants_on_step_3(request, -1)


def search_step_3(request: WSGIRequest) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.search_step_3(request, -1)
