from main.views.auxiliary_general_methods import *
from main.models import CreatedPoll, Poll
from django.shortcuts import redirect, render
from django.template.response import SimpleTemplateResponse


def polls_view(request) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    args = {
        'title': "Опросы",
        'data': {
            'polls': _build_my_polls(profile),
        },
    }
    return render(request, 'main/poll/polls_view.html', args)


def _build_my_polls(profile: Profile) -> list:
    created_polls = CreatedPoll.objects.filter(profile=profile)
    result_polls = []
    for created_poll in created_polls:
        collected_poll = _build_poll(created_poll.poll)
        result_polls.append(collected_poll)
    return result_polls


def _build_poll(poll: Poll):
    collected_poll = {
        'title': poll.name_poll,
        'answers_count': poll.count_passed,
        'date': poll.creation_date,
        'url': '/poll/result/{}/'.format(poll.id)
    }
    if poll.color is not None:
        collected_poll['color'] = poll.color
    target = poll.target
    collected_poll['target'] = {
        'name': target.name,
        'surname': target.surname,
        'patronymic': target.patronymic
    }
    return collected_poll


def _pre_render_item_polls(poll: Poll) -> str:
    collected_poll = _build_poll(poll)
    response = SimpleTemplateResponse('main/includes/item_polls.html', collected_poll)
    result = response.rendered_content
    return result
