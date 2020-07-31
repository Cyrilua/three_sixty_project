from main.views.auxiliary_general_methods import *
from main.models import Poll, CreatedPoll
from django.shortcuts import redirect, render


def polls_view(request) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {}

    return render(request, 'main/poll/polls_view.html', {})


def _build_my_polls(profile: Profile):
    polls = CreatedPoll.objects.filter(profile=profile)

