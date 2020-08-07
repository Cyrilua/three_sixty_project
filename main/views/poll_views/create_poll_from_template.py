from main.views.auxiliary_general_methods import *
from main.models import Poll, TemplatesPoll, Questions, Settings
from django.shortcuts import redirect, render


def create_poll_from_template(request, template_id) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        template: TemplatesPoll = TemplatesPoll.objects.get(id=template_id)
    except ObjectDoesNotExist:
        print('does not exist')
        return redirect('/')

    if template.owner is not None and template.owner != get_user_profile(request):
        print('is not owner')
        return redirect('/')

    args = {
        'title': "Создание опроса из шаблона",
        'poll': _build_template(template)
    }
    print(args['poll'])

    return render(request, 'main/poll/new_poll_editor.html', args)


def _build_template(template: TemplatesPoll) -> dict:
    result = {
        'color': '' if template.color is None else template.color,
        'name': template.name_poll,
        'description': template.description,
        'questions': _build_questions(template.questions.all())
    }
    return result


def _build_questions(questions: list) -> list:
    result = []
    for question in questions:
        question: Questions
        settings: Settings = question.settings
        answers = settings.answer_choice.all()
        collected_question = {
            'type': settings.type,
            'id': question.id,
            'name': question.text,
            'answers': answers,
            'countAnswers': answers.count(),
            'slider': {
                'min': settings.min,
                'max': settings.max,
                'step': settings.step
            }
        }
        result.append(collected_question)
    return result
