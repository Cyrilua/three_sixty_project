from main.views.auxiliary_general_methods import *
from main.models import Poll, CreatedPoll
from django.shortcuts import redirect, render
from django.core.handlers.wsgi import WSGIRequest


def result_poll(request: WSGIRequest, poll_id: int) -> render:
    try:
        poll = Poll.objects.get(id=poll_id)
    except ObjectDoesNotExist:
        # todo throw exception
        return redirect('/')

    profile = get_user_profile(request)
    if poll.initiator != profile:
        #todo throw exception
        pass
    target: Profile = poll.target
    args = {
        'poll': {
            'countAnswers': poll.count_passed,
            'color': poll.color,
            'name': poll.name_poll,
            'target': {
                'href': '/{}/'.format(target.id),
                'name': target.name,
                'surname': target.surname,
                'patronymic': target.patronymic
            },
            'dascription': poll.description,
        }
    }
    return render(request, 'main/poll/poll_results.html', args)
