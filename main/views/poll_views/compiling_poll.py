from datetime import datetime

from main.views.auxiliary_general_methods import *
from main.models import Poll, Questions, Settings,  NeedPassPoll, Answers, Choice, OpenQuestion, RangeAnswers
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.template.response import SimpleTemplateResponse
from django.db.models import F


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
        'id': poll.pk,
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
        'questions': build_questions(poll.questions.all())
    }


def build_questions(questions: list) -> list:
    result = []
    for question in questions:
        question: Questions
        settings: Settings = question.settings
        answers = settings.answer_choice.all()
        collected_question = {
            'type': settings.type,
            'id': question.pk,
            'name': question.text,
            'countAnswers': answers.count(),
            'answer': {
                'min': settings.min,
                'max': settings.max,
                'now': (settings.max + settings.min) / 2 if settings.max is not None else 0
            },
            'answers': answers.values('id', 'text')}
        result.append(collected_question)
    return result


def compiling_poll_link(request: WSGIRequest, poll_id: int, poll_key: int) -> render:
    if auth.get_user(request).is_anonymous:
        return JsonResponse({}, status=404)

    poll = Poll.objects.filter(id=poll_id).first()
    if poll is None:
        return render(request, 'main/error/global_error.html', {'global_error': '404'})

    if poll.key != poll_key:
        return render(request, 'main/error/global_error.html', {'global_error': '400'})

    return redirect('/poll/compiling_poll/{}/'.format(poll.pk))


def send_answer(request: WSGIRequest, poll_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        poll = Poll.objects.filter(id=poll_id)
        if poll.first() is None:
            return JsonResponse({}, status=400)

        _collect_answers(request, poll.first().questions.all().count())
        poll.update(count_passed=F('count_passed') + 1)
        # todo only for debug
        #NeedPassPoll.objects.filter(poll=poll.first(), profile=get_user_profile(request)).delete()
        return JsonResponse({}, status=200)


def _collect_answers(request: WSGIRequest, count_answers: int):
    data = request.POST
    for i in range(count_answers):
        key = 'answers[{}]'.format(i) + '[{}]'
        try:
            question_id = data[key.format('id')]
            question: Questions = Questions.objects.get(id=question_id)
            type_question = data[key.format('type')]
        except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
            continue
        answer = Answers.objects.filter(question=question)
        answer.update(count_profile_answers=F('count_profile_answers') + 1)
        if type_question == 'radio':
            id_choices_answers = data[key.format('value')]
            Choice.objects.filter(answer_choice_id=id_choices_answers).update(count=F('count') + 1)
        elif type_question == 'checkbox':
            list_id_choices_answers = [int(i) for i in data.getlist(key.format('value') + '[]')]
            Choice.objects.filter(answer_choice_id__in=list_id_choices_answers).update(count=F('count') + 1)
        elif type_question == 'range':
            value_range = data[key.format('value')]
            answer.update(range_sum=F('range_sum') + value_range)

            range_answer = RangeAnswers.objects.filter(answer=answer.first(), position_on_range=value_range)
            if range_answer.first() is not None:
                range_answer.update(count=F('count') + 1)
            else:
                range_answer = RangeAnswers()
                range_answer.answer = answer.first()
                range_answer.count = 1
                range_answer.position_on_range = value_range
                range_answer.save()

        elif type_question == 'openQuestion':
            text = data[key.format('value')]
            new_open_question = OpenQuestion()
            new_open_question.text = text
            new_open_question.save()
            answer.first().open_answer.add(new_open_question)
        else:
            continue
