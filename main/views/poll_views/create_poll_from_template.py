from datetime import datetime

from main.views.auxiliary_general_methods import *
from main.models import Poll, TemplatesPoll, Questions, Settings, Group, Moderator, SurveyWizard, Company, AnswerChoice
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.template.response import SimpleTemplateResponse


def create_poll_from_template(request, template_id) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        template: TemplatesPoll = TemplatesPoll.objects.get(id=template_id)
    except ObjectDoesNotExist:
        return redirect('/')

    if template.owner is not None and template.owner != get_user_profile(request):
        return redirect('/')
    profile = get_user_profile(request)
    args = {
        'title': "Создание опроса из шаблона",
        'poll': _build_template(template),
        'is_master': SurveyWizard.objects.filter(profile=profile).exists()
    }

    return render(request, 'main/poll/new_poll_editor.html', args)


def _build_template(template: TemplatesPoll) -> dict:
    result = {
        'color': '' if template.color is None else template.color,
        'name': template.name_poll,
        'description': template.description,
        'questions': _build_questions(template.questions.all(), True),
        'id': template.id,
    }
    return result


def _build_questions(questions: list, from_template: bool) -> list:
    result = []
    for question in questions:
        question: Questions
        settings: Settings = question.settings
        answers = settings.answer_choice.all()
        collected_question = {
            'is_template': True,
            'type': settings.type,
            'id': question.id if not from_template else '',
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


def save_template(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
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
        count_questions = int(data['template[countQuestion]'])
    except ValueError:
        return None
    version = 0
    for question_number in range(count_questions):
        data_key = 'template[questions][{}]'.format(question_number) + '[{}]'
        try:
            question_id = int(data[data_key.format('id')])
            question: Questions = Questions.objects.get(id=question_id)
            version = question.version + 1
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            question = Questions()
        question.text = data[data_key.format('name')]
        settings = _create_or_change_settings(request, question_number, question)
        question.settings = settings
        question.version = version
        question.save()
        poll.questions.add(question)
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


def _build_team_list(teams: (list, filter)) -> list:
    result = []
    for team in teams:
        team: Group
        profiles = team.profile_set.all()
        collected_poll = {
            'id': team.id,
            'name': team.name,
            'numbers': profiles.count(),
            'descriptions': team.description,
            'participants': _build_team_profiles_list(profiles, team),
            'href': ''
        }
        result.append(collected_poll)
    return result


def _build_team_profiles_list(profiles: (list, filter), group, checked_profile: Profile = None) -> list:
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
            'is_leader': group.owner == profile,
            'positions': [i.name for i in profile.positions.all()],
            'platforms': [i.name for i in profile.platforms.all()],
            'is_checked': profile == checked_profile if checked_profile is not None else False
        }
        result.append(collected_profile)

    return result


def _get_roles(profile: Profile) -> list:
    roles = []
    if profile.company.owner.id == profile.id:
        roles.append('boss')
    if SurveyWizard.objects.filter(profile=profile).exists():
        roles.append('master')
    if Moderator.objects.filter(profile=profile).exists():
        roles.append('moderator')
    return roles


def render_category_teams_on_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        profile = get_user_profile(request)
        company = profile.company
        if SurveyWizard.objects.filter(profile=profile).exists():
            teams = company.group_set.all()
        else:
            teams = profile.groups.all()
        collected_teams = _build_team_list(teams)
        content_teams_args = {
            'teams': collected_teams
        }
        content = SimpleTemplateResponse('main/poll/select_target/content_teams.html',
                                         content_teams_args).rendered_content
        return JsonResponse({'content': content}, status=200)


def render_category_participants_on_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        profile = get_user_profile(request)
        company = profile.company
        profiles = company.profile_set.all()
        content_participants_args = {
            'participants': _build_team_profiles_list(profiles, company)
        }
        content = SimpleTemplateResponse('main/poll/select_target/content_participants.html',
                                         content_participants_args).rendered_content
        args = {
            'content': content
        }
        return JsonResponse(args, status=200)


def search_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        print(request.POST)
        mode = request.POST['mode']
        user_input: str = request.POST['input']
        profile = get_user_profile(request)
        if mode == 'participants':
            def compare_with_user_input(profile_compared: Profile):
                for user_input_object in user_input_list:
                    compare = profile_compared.name.find(user_input_object) != -1 or \
                              profile_compared.surname.find(user_input_object) != -1 or \
                              profile_compared.patronymic.find(user_input_object) != -1
                    if compare:
                        return True
                return False
            user_input_list = user_input.split(' ')
            #profiles = profile.company.profile_set.all()
            #profiles = filter(lambda x: compare_with_user_input(x), profiles)
            print(type(user_input_list))
            print(user_input_list)
            profiles = profile.company.profile_set.all().filter(name__in__icontains=user_input_list)
            print(profiles)
            content_participants_args = {
                'participants': _build_team_profiles_list(profiles, profile.company)
            }
            content = SimpleTemplateResponse('main/poll/select_target/content_participants.html',
                                             content_participants_args).rendered_content
        elif mode == 'teams':
            user_is_master = SurveyWizard.objects.filter(profile=profile).exists()
            if user_is_master:
                teams = Group.objects.filter(company=profile.company)
            else:
                teams = profile.groups.all()
            teams = filter(lambda team: team.name.find(user_input) != -1, teams)
            collected_teams = _build_team_list(teams)
            content_teams_args = {
                'teams': collected_teams
            }
            content = SimpleTemplateResponse('main/poll/select_target/content_teams.html',
                                             content_teams_args).rendered_content
        else:
            return JsonResponse({}, status=400)
        return JsonResponse({'content': content}, status=200)


def render_step_2_from_step_3(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        print(request.POST)
        return JsonResponse({}, status=200)


def render_step_1_from_step_3(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        # TODO
        return JsonResponse({}, status=200)


def render_step_3_from_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        try:
            poll_id = int(request.POST['pollId'])
            poll = Poll.objects.get(id=poll_id)
            profile_id = int(request.POST['checkedTarget'])
            profile = Profile.objects.get(id=profile_id)
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            return JsonResponse({}, status=400)
        poll.target = profile
        poll.save()
        # TODO
        return JsonResponse({}, status=200)


def render_step_3_from_step_1(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        # TODO
        return JsonResponse({}, status=200)


def render_step_1_from_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        try:
            poll_id = int(request.POST['pollId'])
            poll = Poll.objects.get(id=poll_id)
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            return JsonResponse({}, status=400)

        try:
            profile_id = int(request.POST['checkedTarget'])
            profile = Profile.objects.get(id=profile_id)
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            pass
        else:
            poll.target = profile
            poll.save()

        categories = SimpleTemplateResponse('main/poll/editor/editor_content.html',
                                            {'poll': _build_created_poll(poll)}).rendered_content
        head_move = SimpleTemplateResponse('main/poll/editor/editor_head_move.html').rendered_content
        head_main = SimpleTemplateResponse('main/poll/editor/editor_head_main.html').rendered_content
        args = {
            'categories': categories,
            'headMove': head_move,
            'headMain': head_main
        }
        return JsonResponse(args, status=200)


def _build_created_poll(poll: Poll) -> dict:
    result = {
        'color': '' if poll.color is None else poll.color,
        'name': poll.name_poll,
        'description': poll.description,
        'questions': _build_questions(poll.questions.all(), False),
        'id': poll.id,
    }
    return result


def render_step_2_from_step_1(request: WSGIRequest, template_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        try:
            poll_id = int(request.POST['pollId'])
            poll = Poll.objects.get(id=poll_id)
            poll = _create_or_change_poll(request, poll)
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            poll = _create_or_change_poll(request, None)
        version = _create_new_questions_or_change(request, poll)
        _delete_deleted_questions(poll, version)

        head_main = SimpleTemplateResponse('main/poll/select_target/select_target_head_main.html', {}).rendered_content
        head_move = SimpleTemplateResponse('main/poll/select_target/select_target_head_move.html', {}).rendered_content
        profile = get_user_profile(request)
        company: Company = profile.company
        profiles = company.profile_set.all()
        categories_args = {
            'participants': _build_team_profiles_list(profiles, company, poll.target),
            'company': {
                'countParticipants': profiles.count(),
            }
        }
        if SurveyWizard.objects.filter(profile=profile).exists():
            categories_args['company']['countTeams'] = Group.objects.filter(company=company).count()
        else:
            categories_args['company']['countTeams'] = profile.groups.all().count()

        categories = SimpleTemplateResponse('main/poll/select_target/select_target_content.html',
                                            categories_args).rendered_content

        args = {
            'pollId': poll.id,
            'headMain': head_main,
            'headMove': head_move,
            'categories': categories
        }
        return JsonResponse(args, status=200)


def _create_or_change_poll(request: WSGIRequest, poll: Poll) -> Poll:
    if poll is None:
        poll = Poll()
    data = request.POST
    data_key = 'template[{}]'
    poll.name_poll = data[data_key.format('name')]
    poll.description = data[data_key.format('description')]
    poll.color = data[data_key.format('color')]
    poll.creation_date = datetime.today()
    poll.initiator = get_user_profile(request)
    poll.save()
    return poll


def _delete_deleted_questions(poll: Poll, version: int) -> None:
    questions = poll.questions.all().filter(version__lt=version)
    for question in questions:
        question.delete()
