from main.views.auxiliary_general_methods import *
from main.models import Poll, CreatedPoll, Answers, Choice, RangeAnswers
from django.shortcuts import redirect, render
from django.core.handlers.wsgi import WSGIRequest


def result_poll(request: WSGIRequest, poll_id: int) -> render:
    poll = Poll.objects.filter(id=poll_id).first()
    if poll is None:
        return render(request, 'main/errors/global_error.html', {'global_error': '404'})

    profile = get_user_profile(request)
    if poll.initiator != profile or poll.count_passed < 2:
        return render(request, 'main/errors/global_error.html', {
            'global_error': "custom",
            "global_error_info": "Результаты опроса ещё недоступны, нужно дождаться большего количества ответов",
            "back_page": {
                'href': "/polls/",
                'text': "К опросам"
            },
        })

    target: Profile = poll.target
    args = {
        'poll': {
            'countAnswers': poll.count_passed,
            'color': poll.color,
            'name': poll.name_poll,
            'target': {
                'href': '/{}/'.format(target.pk),
                'name': target.name,
                'surname': target.surname,
                'patronymic': target.patronymic
            },
            'dascription': poll.description,
            'questions': _build_questions(poll)
        }
    }
    CreatedPoll.objects.filter(profile=profile, poll=poll).update(is_viewed=True)
    return render(request, 'main/poll/poll_results.html', args)


def _build_questions(poll: Poll) -> list:
    result = []
    for answer in poll.answers_set.all():
        answer: Answers
        completed_question = {
            'type': answer.question.settings.type,
            'name': answer.question.text,
            'answers': _build_answers_choices(answer),
        }
        result.append(completed_question)
    return result


def _build_answers_choices(answer: Answers) -> list:
    result = []

    if answer.question.settings.type == 'range':
        for range_answer in RangeAnswers.objects.filter(answer=answer):
            range_answer: RangeAnswers
            percent = "%.2f" % ((range_answer.count * 100) / answer.count_profile_answers)
            result.append({
                'countAnswer': range_answer.count,
                'percent': percent,
                'value': range_answer.position_on_range
            })
        return result

    if answer.question.settings.type == 'openQuestion':
        return answer.open_answer.all()

    count_profile_answers = answer.count_profile_answers
    if answer.question.settings.type == 'checkbox':
        count_profile_answers = 0
        for i in answer.choices.all():
            count_profile_answers += i.count
    for choice in answer.choices.all():
        choice: Choice
        try:
            percent = (choice.count * 100) / count_profile_answers
            value = answer.range_sum // count_profile_answers
        except ZeroDivisionError:
            percent = 0
            value = 0
        completed_choice = {
            'text': choice.answer_choice.text,
            'result': {
                'countAnswer': choice.count,
                'percent': "%.2f" % percent,
                'value': value,
            }
        }
        result.append(completed_choice)

    return result
