from main.views.auxiliary_general_methods import *
from main.models import Poll, Draft


def choose_poll(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {
        'title': "Опросы",
        'companys': build_company(request),
        'teams': build_teams(request)
    }

    return render(request, 'main/poll/new_poll_view.html', args)


def build_company(request):
    company = get_user_profile(request).company
    result = [{
        'name': company.name,
        'url': '/respondent_choice_c/',
    }]
    return result


def build_teams(request):
    profile = get_user_profile(request)
    result = []
    for group in profile.groups.all():
        result.append({
            'name': group.name,
            'url': '/respondent_choice_t/{}/'.format(group.id),
        })
    return result


def poll_create(request, poll_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        poll = Poll.objects.get(id=poll_id)
    except:
        print('poll does not exist')
        return redirect('/')
    if poll.initiator.id != auth.get_user(request).id:
        print('I am not an initiator')
        return redirect('/')

    questions = poll.questions_set.all()

    if len(questions) == 0:
        first_question = {
            'type': 'radio',
            'text': '',
            'answers': {
                'text': ''
            }
        }
        questions = [first_question]
    else:
        questions = build_questions(poll)

    args = {
        'poll': {
            'status': 'edit',
            'data': {
                'questions': questions
            },
        }
    }

    if request.method == "POST":
        print()
        print('I am in POST')
        print()

    if request.is_ajax():
        print()
        print('I am in AJAX')
        print()

    return render(request, 'main/poll/poll_editor.html', args)


def build_questions(questions):
    result = []

    for question in questions:
        type = question.settings.type
        build_question = {
            'type': type,
            'text': question.text
        }

        if type == 'radio' or type == 'checkbox':
            build_question['answers'] = []
            number = 1
            for answer in question.settings.answer_choice.all():
                build_question['answers'].append({
                    'number': number,
                    'text': answer.text
                })
                number += 1
        elif type == 'range':
            settings = question.settings
            build_question['range'] = {
                'min': settings.min,
                'max': settings.max,
                'step': settings.step
            }
    return result


def poll_create_redirect(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    draft_polls = list(Draft.objects.get(profile=profile).poll.all())
    if len(draft_polls) == 0:
        poll = Poll()
        poll.initiator = auth.get_user(request)
        poll.save()

        draft = Draft()
        draft.profile = profile
        draft.save()

        draft.poll.add(poll)
        draft.save()
        return redirect('/poll/editor/{}/'.format(poll.id))

    return redirect('/poll/editor/{}/'.format(draft_polls[0].id))