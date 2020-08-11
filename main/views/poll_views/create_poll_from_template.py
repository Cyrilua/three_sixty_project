from main.views.auxiliary_general_methods import *
from main.models import Poll, TemplatesPoll, Questions, Settings, Group, Moderator, SurveyWizard, Company
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest


def create_poll_from_template(request, template_id) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        template: TemplatesPoll = TemplatesPoll.objects.get(id=template_id)
    except ObjectDoesNotExist:
        return redirect('/')

    if template.owner is not None and template.owner != get_user_profile(request):
        return redirect('/')

    args = {
        'title': "Создание опроса из шаблона",
        'poll': _build_template(template)
    }

    return render(request, 'main/poll/new_poll_editor.html', args)


def _build_template(template: TemplatesPoll) -> dict:
    result = {
        'color': '' if template.color is None else template.color,
        'name': template.name_poll,
        'description': template.description,
        'questions': _build_questions(template.questions.all()),
        'id': template.id,
    }
    return result


def _build_questions(questions: list) -> list:
    result = []
    for question in questions:
        question: Questions
        settings: Settings = question.settings
        answers = settings.answer_choice.all()
        collected_question = {
            'is_template': True,
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


def save_template(request: WSGIRequest) -> JsonResponse:
    if request.is_ajax():
        print(request.POST)
        for i in request.POST:
            print(i)
        data = request.POST
        print(request.POST['template[questions][0][countAnswers]'])
        for i in data['template[questions][1][answers][]'].all():
            print(i)
        return JsonResponse({}, status=200)


def _create_new_template(request: WSGIRequest) -> TemplatesPoll:
    data = request.POST
    data_key = 'template[{}]'
    new_template = TemplatesPoll()
    new_template.name_poll = data[data_key.format('name')]
    new_template.description = data[data_key.format('description')]
    new_template.owner = get_user_profile(request)
    new_template.color = data[data_key.format('color')]
    new_template.save()
    return new_template


def _create_new_questions_for_template(request: WSGIRequest, template: TemplatesPoll) -> None:
    data = request.POST
    for i in range(data['template[questions]']):
        data_key = 'template[questions][{}]'.format(i) + '[{}]'
        question = Questions()
        question.text = data[data_key.format('name')]


def _create_settings(request: WSGIRequest, question_number: int):
    def add_if_contains_key(key: str):
        key = "template[questions][{}]".format(question_number) + key
        return data[key] if key in keys else None
    data = request.POST
    keys = data.keys()
    data_key = "template[questions][{}]".format(question_number) + '[{}]'
    settings = Settings()
    settings.type = data[data_key.format('type')]
    settings.step = add_if_contains_key('[settingsSlider][step]')
    settings.min = add_if_contains_key('[settingsSlider][min]')
    settings.max = add_if_contains_key('[settingsSlider][max]')
    settings.save()




def render_teams_list_for_choose_respondents(request, template_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        print(request.POST)
    profile = get_user_profile(request)
    company = profile.company
    teams = profile.groups.all()
    args = {
        'company': {
            'countTeams': teams.count(),
            'countParticipants': company.profile_set.all().count()
        }
    }
    return JsonResponse({}, status=200)


def _build_team_list(teams: list) -> list:
    result = []
    for team in teams:
        team: Group
        profiles = team.profile_set.all()
        collected_poll = {
            'id': team.id,
            'name': team.name,
            'numbers': profiles.count(),
            'descriptions': team.description,
            'participants': _build_team_profiles_list(profiles)
        }
        result.append(collected_poll)
    return result


def _build_team_profiles_list(profiles: list, team: Group) -> list:
    result = []
    for profile in profiles:
        profile: Profile
        collected_profile = {
            'href': '/{}/'.format(profile.id),
            'id': profile.id,
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic,
            'roles': _get_roles(profile),
            'is_leader': team.owner == profile,
            'positions': [i.name for i in profile.positions.all()],
            'platforms': [i.name for i in profile.platforms.all()],
        }
        result.append(collected_profile)

    return result


def _get_roles(profile: Profile) -> list:
    roles = []
    if profile.company.owner.id == profile.id:
        roles.append('boss')
    if SurveyWizard.objects.filter(profile=profile).exist():
        roles.append('master')
    if Moderator.objects.filter(profile=profile).exist():
        roles.append('moderator')
    return roles
