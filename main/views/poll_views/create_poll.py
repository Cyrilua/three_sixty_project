from main.views.auxiliary_general_methods import *
from main.models import SurveyWizard, Poll, Group
from django.shortcuts import redirect, render
from django.http import JsonResponse
from . import create_poll_from_template
from django.core.handlers.wsgi import WSGIRequest


def redirect_for_create(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    new_poll = Poll()
    new_poll.initiator = profile
    new_poll.save()
    return redirect('/poll/editor/{}/'.format(new_poll.pk))


def create_new_poll_from_company(request, company_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    company = Company.objects.filter(id=company_id).first()
    if company is None:
        return render(request, 'main/errors/global_error.html', {'global_error': '404'})

    profile = get_user_profile(request)
    if not company.profile_set.filter(id=profile.pk).exists():
        return render(request, 'main/errors/global_error.html', {'global_error': '403'})

    new_poll = Poll()
    new_poll.initiator = profile
    new_poll.start_from = 'company'
    new_poll.from_id_group = company.pk
    new_poll.save()
    return redirect('/poll/editor/{}/'.format(new_poll.pk))


def poll_create_from_team(request, team_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    team = Group.objects.filter(id=team_id).first()
    if team is None:
        return render(request, 'main/errors/global_error.html', {'global_error': '404'})

    profile = get_user_profile(request)
    if not team.profile_set.filter(id=profile.pk).exists():
        return render(request, 'main/errors/global_error.html', {'global_error': '403'})

    new_poll = Poll()
    new_poll.initiator = profile
    new_poll.start_from = 'team'
    new_poll.from_id_group = team.pk
    new_poll.save()
    return redirect('/poll/editor/{}/'.format(new_poll.pk))


def poll_create(request, poll_id: int):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    poll = Poll.objects.filter(id=poll_id).first()
    if poll.initiator != profile:
        return render(request, 'main/errors/global_error.html', {'global_error': '400'})
    args = {
        'title': "Создание нового опроса",
        'poll': build_poll(poll),
        'profile': get_header_profile(profile),
    }
    if SurveyWizard.objects.filter(profile=profile).exists():
        args['is_master'] = 'is_master'

    return render(request, 'main/poll/new_poll_editor.html', args)


def build_poll(poll: Poll) -> dict:
    result = {
        'id': poll.pk,
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


def save_template(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.save_template(request, -1)


def render_category_teams_on_step_2(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_category_teams_on_step_2(request, -1)


def render_category_participants_on_step_2(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_category_participants_on_step_2(request, -1)


def search_step_2(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.search_step_2(request, -1)


def render_step_2_from_step_3(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_2_from_step_3(request, -1)


def render_step_1_from_step_3(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_1_from_step_3(request, -1)


def render_step_1_from_step_3_not_master(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    return render_step_1_from_step_3(request, -1)


def render_step_3_from_step_2(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_3_from_step_2(request, -1)


def render_step_3_from_step_1(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_3_from_step_1(request, -1)


def render_step_3_from_step_1_not_master(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_3_from_step_1_not_master(request, -1)


def render_step_1_from_step_2(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_1_from_step_2(request, -1)


def render_step_2_from_step_1(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_step_2_from_step_1(request, -1)


def poll_preview(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.poll_preview(request, -1)


def poll_editor(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.poll_editor(request, -1)


def cancel_created_poll(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.cancel_created_poll(request, -1)


def send_poll(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.send_poll(request, -1)


def render_category_teams_on_step_3(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_category_teams_on_step_3(request, -1)


def render_category_participants_on_step_3(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.render_category_participants_on_step_3(request, -1)


def search_step_3(request: WSGIRequest, poll_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        return create_poll_from_template.search_step_3(request, -1)
