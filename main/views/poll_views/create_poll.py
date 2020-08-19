from main.views.auxiliary_general_methods import *
from main.models import SurveyWizard
from django.shortcuts import redirect, render


def poll_create(request):
    # TODO
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
        'color': 'blue',
        #'name': poll.name_poll,
        #'description': poll.description,
        'questions': build_questions(),
        #'id': poll.pk,
    }
    return result


def build_questions() -> list:
    result = []
    collected_question = {
        'is_template': True,
        'type': 'checkbox',
        #'id': question.pk if not from_template else '',
        #'name': question.text,
        #'answers': answers,
        'countAnswers': 0,
    }
    result.append(collected_question)
    return result
