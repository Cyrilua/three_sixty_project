from main.views.auxiliary_general_methods import *
from main.models import Poll, CreatedPoll
from django.shortcuts import redirect, render


def result_poll(request, poll_id: int) -> render:
    return render(request, 'main/poll/old/poll_results.html', {})
