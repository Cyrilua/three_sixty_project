from datetime import datetime

from main.views.auxiliary_general_methods import *
from main.models import Poll, TemplatesPoll, Questions, Settings, AnswerChoice, SurveyWizard
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.template.response import SimpleTemplateResponse
from .choose_target import save_information as save_information_from_step_2
from .start_create import build_questions, build_poll


def save_template(request: WSGIRequest) -> JsonResponse:
    # todo за одно создание опроса - один шаблон (изменять уже сохраненный на этапе создания шаблон)
    template = _create_new_template(request)
    _create_new_questions_or_change(request, template)
    return JsonResponse({}, status=200)


def _create_new_template(request: WSGIRequest) -> TemplatesPoll:
    data = request.POST
    data_key = 'template[{}]'
    new_template = TemplatesPoll()
    new_template.name_poll = data[data_key.format('name')]
    new_template.description = data[data_key.format('description')]
    new_template.owner = get_user_profile(request)
    new_template.color = None if data[data_key.format('color')] == '' else data[data_key.format('color')]
    new_template.save()
    return new_template


def _create_new_questions_or_change(request: WSGIRequest, poll: (TemplatesPoll, Poll)) -> int:
    data = request.POST
    try:
        if data['category'] == 'preview':
            return poll
    except MultiValueDictKeyError:
        pass
    try:
        count_questions = int(data['template[countQuestion]'])
    except ValueError:
        return None
    first_question = poll.questions.all().first()
    version = 0 if first_question is None else first_question.version + 1
    ordinal_number = 0
    for question_number in range(count_questions):
        data_key = 'template[questions][{}]'.format(question_number) + '[{}]'
        try:
            question_id = int(data[data_key.format('id')])
            question: Questions = Questions.objects.get(id=question_id)
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            question = Questions()
        question.text = data[data_key.format('name')]
        settings = _create_or_change_settings(request, question_number, question)
        question.settings = settings
        question.version = version
        question.ordinal_number = ordinal_number
        question.save()
        poll.questions.add(question)
        ordinal_number += 1
    return version


def _create_or_change_settings(request: WSGIRequest, question_number: int, question: Questions) -> Settings:
    def add_if_contains_key(key: str):
        key = "template[questions][{}]".format(question_number) + key
        return data[key] if key in keys else None

    data = request.POST
    keys = data.keys()
    data_key = "template[questions][{}]".format(question_number) + '[{}]'
    if question.settings is None:
        settings = Settings()
    else:
        settings = question.settings
    settings.type = data[data_key.format('type')]
    settings.step = add_if_contains_key('[settingsSlider][step]')
    settings.min = add_if_contains_key('[settingsSlider][min]')
    settings.max = add_if_contains_key('[settingsSlider][max]')
    settings.save()

    try:
        count_answers = int(request.POST[data_key.format('countAnswers')])
        data_key = data_key.format('answers') + "[{}]"
    except (ValueError, MultiValueDictKeyError):
        pass
    else:
        for answer_number in range(count_answers):
            answer_number: int
            current_data_key = data_key.format(answer_number) + '[{}]'
            try:
                answer_id = int(data[current_data_key.format('id')])
                answer = AnswerChoice.objects.get(id=answer_id)
            except (ValueError, MultiValueDictKeyError, ObjectDoesNotExist):
                answer = AnswerChoice()
            answer.text = data[current_data_key.format('text')]
            answer.save()
            settings.answer_choice.add(answer)
    return settings


def save_information(request: WSGIRequest) -> Poll:
    try:
        category = request.POST['category']
    except MultiValueDictKeyError:
        return None
    try:
        poll_id = int(request.POST['pollId'])
        poll = Poll.objects.get(id=poll_id)
    except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
        poll = Poll()
    if category == "editor":
        poll = _create_or_change_poll(request, poll)
        version = _create_new_questions_or_change(request, poll)
        poll.questions.all().exclude(version=version).delete()
        return poll
    elif category == "preview":
        return poll
    return None


def _create_or_change_poll(request: WSGIRequest, poll: Poll) -> Poll:
    data = request.POST
    data_key = 'template[{}]'
    poll.name_poll = data[data_key.format('name')]
    poll.description = data[data_key.format('description')]
    poll.color = data[data_key.format('color')]
    poll.creation_date = datetime.today()
    profile = get_user_profile(request)
    if not SurveyWizard.objects.filter(profile=profile).exists():
        poll.target = profile
    poll.initiator = profile
    poll.save()
    return poll


def get_rendered_page(request: WSGIRequest, poll: Poll) -> dict:
    created_poll = build_poll(poll)
    categories = SimpleTemplateResponse('main/poll/editor/editor_content.html',
                                        {'poll': created_poll}).rendered_content
    args = {}
    profile = get_user_profile(request)
    if SurveyWizard.objects.filter(profile=profile).exists():
        args['is_master'] = 'is_master'
    head_move = SimpleTemplateResponse('main/poll/editor/editor_head_move.html', args).rendered_content
    head_main = SimpleTemplateResponse('main/poll/editor/editor_head_main.html', args).rendered_content
    return {
        'categories': categories,
        'headMove': head_move,
        'headMain': head_main
    }


def poll_preview(request: WSGIRequest) -> JsonResponse:
    try:
        poll_id = int(request.POST['pollId'])
        poll = Poll.objects.get(id=poll_id)
        poll = _create_or_change_poll(request, poll)
    except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
        poll = _create_or_change_poll(request, Poll())
    version = _create_new_questions_or_change(request, poll)
    poll.questions.all().exclude(version=version).delete()
    created_poll = build_poll(poll)
    if poll.target is not None:
        created_poll['target'] = {
            'name': poll.target.name,
            'surname': poll.target.surname,
            'patronymic': poll.target.patronymic
        }
    content = SimpleTemplateResponse('main/poll/taking_poll_preview.html',
                                     {'poll': created_poll}).rendered_content
    return JsonResponse({'content': content, 'pollId': poll.pk}, status=200)


def poll_editor(request: WSGIRequest) -> JsonResponse:
    try:
        poll_id = int(request.POST['pollId'])
        poll = Poll.objects.get(id=poll_id)
    except (MultiValueDictKeyError, ObjectDoesNotExist):
        return JsonResponse({}, status=400)
    created_poll = build_poll(poll)
    content = SimpleTemplateResponse('main/poll/editor/content_poll_editor.html',
                                     {'poll': created_poll}).rendered_content
    return JsonResponse({'content': content}, status=200)
