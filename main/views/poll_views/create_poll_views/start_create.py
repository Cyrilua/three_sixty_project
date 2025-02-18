from main.models import Poll, TemplatesPoll, Questions, Settings


def build_poll(poll: (TemplatesPoll, Poll)) -> dict:
    is_template = type(poll) is TemplatesPoll
    result = {
        'color': '' if poll.color is None else poll.color,
        'name': poll.name_poll if poll.name_poll is not None else '',
        'description': poll.description if poll.description is not None else '',
        'questions': build_questions(poll.questions.all(), is_template),
    }
    return result


def build_questions(questions: list, from_template: bool) -> list:
    result = []
    for question in questions:
        question: Questions
        settings: Settings = question.settings
        answers = settings.answer_choice.all()
        collected_question = {
            'is_template': True,
            'type': settings.type,
            'id': question.pk if not from_template else '',
            'name': question.text,
            'countAnswers': answers.count(),
            'slider': {
                'min': settings.min,
                'max': settings.max,
                'step': settings.step
            },
        }
        if from_template:
            collected_question['answers'] = answers.values('text')
        else:
            collected_question['answers'] = answers.values('id', 'text')
        result.append(collected_question)
    return result
