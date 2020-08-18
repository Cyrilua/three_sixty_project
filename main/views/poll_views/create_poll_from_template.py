from datetime import datetime

from main.views.auxiliary_general_methods import *
from main.models import Poll, TemplatesPoll, Questions, Settings, Group, Moderator, SurveyWizard, Company, \
    AnswerChoice, NeedPassPoll, CreatedPoll
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.template.response import SimpleTemplateResponse
from django.db.models import Q
from django.db.models.query import QuerySet
from django.core.mail import EmailMessage


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
        'poll': _build_poll(template),
    }
    if SurveyWizard.objects.filter(profile=profile).exists():
        args['is_master'] = 'is_master'

    return render(request, 'main/poll/new_poll_editor.html', args)


def _build_poll(poll: (TemplatesPoll, Poll)) -> dict:
    is_template = type(poll) is TemplatesPoll
    result = {
        'color': '' if poll.color is None else poll.color,
        'name': poll.name_poll,
        'description': poll.description,
        'questions': _build_questions(poll.questions.all(), is_template),
        'id': poll.pk,
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
            'id': question.pk if not from_template else '',
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


def _build_team_list(teams: (list, filter), checked_profiles: list, unbilding_user=None) -> list:
    result = []
    for team in teams:
        team: Group
        profiles = team.profile_set.all()
        collected_poll = {
            'id': team.pk,
            'name': team.name,
            'numbers': profiles.count(),
            'descriptions': team.description,
            'participants': _build_team_profiles_list(profiles, team, checked_profiles, unbilding_user),
            'href': ''
        }
        result.append(collected_poll)
    return result


def _build_team_profiles_list(profiles: (list, filter), group: (Group, Company), checked_profiles: list,
                              unbilding_user=None) -> list:
    result = []
    for profile in profiles:
        if profile == unbilding_user:
            continue
        profile: Profile
        collected_profile = {
            'href': '/{}/'.format(profile.pk),
            'id': profile.pk,
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic,
            'roles': _get_roles(profile),
            'positions': [i.name for i in profile.positions.all()],
            'platforms': [i.name for i in profile.platforms.all()],
            'is_checked': profile in checked_profiles
        }
        if group is not None:
            collected_profile['is_leader'] = group.owner == profile

        result.append(collected_profile)

    return result


def _get_roles(profile: Profile) -> list:
    roles = []
    if profile.company.owner.pk == profile.pk:
        roles.append('boss')
    if SurveyWizard.objects.filter(profile=profile).exists():
        roles.append('master')
    if Moderator.objects.filter(profile=profile).exists():
        roles.append('moderator')
    return roles


def render_category_teams_on_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        try:
            poll_id = int(request.POST['pollId'])
            poll = Poll.objects.get(id=poll_id)
        except (ValueError, ObjectDoesNotExist, MultiValueDictKeyError):
            return JsonResponse({}, status=400)

        try:
            target_id = int(request.POST['checkedTarget'])
            target = Profile.objects.get(id=target_id)
            poll.target = target
        except (ValueError, ObjectDoesNotExist, MultiValueDictKeyError):
            pass

        content_teams_args = _render_category_teams(request, [poll.target])
        content = SimpleTemplateResponse('main/poll/select_target/content_teams.html',
                                         content_teams_args).rendered_content
        return JsonResponse({'content': content}, status=200)


def _render_category_teams(request: WSGIRequest, checked_profiles) -> dict:
    profile = get_user_profile(request)
    company = profile.company
    if SurveyWizard.objects.filter(profile=profile).exists():
        teams = company.group_set.all()
    else:
        teams = profile.groups.all()
    collected_teams = _build_team_list(teams, checked_profiles)
    return {'teams': collected_teams}


def render_category_participants_on_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        try:
            poll_id = int(request.POST['pollId'])
            poll = Poll.objects.get(id=poll_id)
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            return JsonResponse({}, status=400)

        try:
            target_id = int(request.POST['checkedTarget'])
            target = Profile.objects.get(id=target_id)
            poll.target = target
        except (ValueError, ObjectDoesNotExist, MultiValueDictKeyError):
            pass

        content_participants_args = _render_category_participants(request, [poll.target])
        content = SimpleTemplateResponse('main/poll/select_target/content_participants.html',
                                         content_participants_args).rendered_content
        args = {'content': content}
        return JsonResponse(args, status=200)


def _render_category_participants(request: WSGIRequest, list_checked_profiles: list):
    profile = get_user_profile(request)
    company = profile.company
    profiles = company.profile_set.all()
    return {'participants': _build_team_profiles_list(profiles, company, list_checked_profiles)}


def search_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        try:
            poll_id = int(request.POST['pollId'])
            poll = Poll.objects.get(id=poll_id)
        except (MultiValueDictKeyError, ValueError, ObjectDoesNotExist):
            return None

        mode = request.POST['mode']
        user_input: str = request.POST['input']
        profile = get_user_profile(request)
        result_search = _search(mode, user_input, profile)

        if mode == 'participants':
            content_participants_args = {
                'participants': _build_team_profiles_list(result_search, profile.company, [])
            }
            content = SimpleTemplateResponse('main/poll/select_target/content_participants.html',
                                             content_participants_args).rendered_content
        elif mode == 'teams':
            collected_teams = _build_team_list(result_search, [poll.target])
            content_teams_args = {
                'teams': collected_teams
            }
            content = SimpleTemplateResponse('main/poll/select_target/content_teams.html',
                                             content_teams_args).rendered_content
        else:
            return JsonResponse({}, status=400)
        return JsonResponse({'content': content}, status=200)


def _search(mode: str, user_input: str, profile: Profile) -> QuerySet:
    if mode == 'participants':
        user_input_list = user_input.split(' ')
        profiles = profile.company.profile_set.all()
        for input_iter in user_input_list:
            profiles = profiles.filter(
                Q(name__icontains=input_iter) | Q(surname__icontains=input_iter) | Q(patronymic__icontains=input_iter))
        return profiles
    elif mode == 'teams':
        user_is_master = SurveyWizard.objects.filter(profile=profile).exists()
        if user_is_master:
            teams: QuerySet = Group.objects.filter(company=profile.company)
        else:
            teams: QuerySet = profile.groups.all()
        return teams.filter(name__icontains=user_input)


def render_step_2_from_step_3(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = _save_information_from_step_3(request)
        if poll is None:
            return JsonResponse({}, status=400)
        args = _get_rendered_page_for_step_2(request, poll)
        return JsonResponse(args, status=200)


def render_step_1_from_step_3(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = _save_information_from_step_3(request)
        if poll is None:
            return JsonResponse({}, status=400)
        args = _get_rendered_page_for_step_1(request, poll)
        return JsonResponse(args, status=200)


def render_step_1_from_step_3_not_master(request: WSGIRequest, template_id) -> JsonResponse:
    return render_step_1_from_step_3(request, template_id)


def render_step_3_from_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = _save_information_from_step_2(request)
        if poll is None:
            return JsonResponse({}, status=400)
        args = _get_rendered_page_for_step_3(request, poll)
        return JsonResponse(args, status=200)


def _save_information_from_step_3(request: WSGIRequest) -> Poll:
    try:
        poll_id = int(request.POST['pollId'])
        poll = Poll.objects.get(id=poll_id)
        list_profiles = request.POST.getlist('checkedInterviewed[]')
    except (MultiValueDictKeyError, ValueError, ObjectDoesNotExist):
        return None
    first_respondent = NeedPassPoll.objects.filter(poll=poll).first()
    version = 1 if first_respondent is None else first_respondent.version + 1
    for profile_id in list_profiles:
        try:
            profile = Profile.objects.get(id=int(profile_id))
        except (ValueError, ObjectDoesNotExist):
            continue

        try:
            need_pass: NeedPassPoll = NeedPassPoll.objects.get(poll=poll, profile_id=profile_id)
        except ObjectDoesNotExist:
            need_pass = NeedPassPoll()
            need_pass.profile = profile
            need_pass.poll = poll
        need_pass.version = version
        need_pass.save()
    # todo посмотреть работоспособность
    profiles_for_delete = NeedPassPoll.objects.filter(poll=poll).exclude(version=version)
    print(profiles_for_delete)
    #profiles_for_delete.delete()
    return poll


def _get_rendered_page_for_step_3(request: WSGIRequest, poll: Poll):
    args = {}
    profile = get_user_profile(request)
    if SurveyWizard.objects.filter(profile=profile).exists():
        args['is_master'] = 'is_master'
    main = SimpleTemplateResponse('main/poll/select_interviewed/select_interviewed_head_main.html',
                                  args).rendered_content
    move = SimpleTemplateResponse('main/poll/select_interviewed/select_interviewed_head_move.html',
                                  args).rendered_content
    company = profile.company
    target_id = -1 if poll.target is None else poll.target.id
    initiator_id = -1 if poll.initiator is None else poll.initiator.id
    profiles = Profile.objects.filter(company=company).exclude(id=target_id).exclude(id=initiator_id)

    profiles_checked = [i.profile for i in NeedPassPoll.objects.filter(poll=poll)]
    categories_args = {
        'participants': _build_team_profiles_list(profiles, company, profiles_checked),
        'company': {
            'countParticipants': profiles.count(),
        }
    }
    if SurveyWizard.objects.filter(profile=profile).exists():
        categories_args['company']['countTeams'] = Group.objects.filter(company=company).count()
    else:
        categories_args['company']['countTeams'] = profile.groups.all().count()

    categories = SimpleTemplateResponse('main/poll/select_interviewed/select_interviewed_content.html',
                                        categories_args).rendered_content

    return {
        'categories': categories,
        'headMove': move,
        'headMain': main,
        'pollId': poll.pk
    }


def render_step_3_from_step_1(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = _save_information_from_step_1(request)
        if poll is None:
            return JsonResponse({}, status=400)

        args = _get_rendered_page_for_step_3(request, poll)
        return JsonResponse(args, status=200)


def render_step_3_from_step_1_not_master(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = _save_information_from_step_1(request)
        poll.target = get_user_profile(request)
        if poll is None:
            return JsonResponse({}, status=400)

        args = _get_rendered_page_for_step_3(request, poll)
        return JsonResponse(args, status=200)


def render_step_1_from_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = _save_information_from_step_2(request)
        if poll is None:
            return JsonResponse({}, status=400)

        args = _get_rendered_page_for_step_1(request, poll)
        return JsonResponse(args, status=200)


def _save_information_from_step_1(request: WSGIRequest) -> Poll:
    try:
        poll_id = int(request.POST['pollId'])
        poll = Poll.objects.get(id=poll_id)
        poll = _create_or_change_poll(request, poll)
    except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
        poll = _create_or_change_poll(request, None)
    version = _create_new_questions_or_change(request, poll)
    poll.questions.all().exclude(version=version).delete()
    return poll


def _get_rendered_page_for_step_1(request: WSGIRequest, poll: Poll) -> dict:
    created_poll = _build_created_poll(poll)
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


def _build_created_poll(poll: Poll) -> dict:
    result = {
        'color': '' if poll.color is None else poll.color,
        'name': poll.name_poll,
        'description': poll.description,
        'questions': _build_questions(poll.questions.all(), False),
        'id': poll.pk,
    }
    return result


def render_step_2_from_step_1(request: WSGIRequest, template_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        poll = _save_information_from_step_1(request)
        if poll is None:
            return JsonResponse({}, status=400)
        args = _get_rendered_page_for_step_2(request, poll)
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
    profile = get_user_profile(request)
    if not SurveyWizard.objects.filter(profile=profile).exists():
        poll.target = profile
    poll.initiator = profile
    poll.save()
    return poll


def _save_information_from_step_2(request: WSGIRequest) -> Poll:
    try:
        poll_id = int(request.POST['pollId'])
        poll = Poll.objects.get(id=poll_id)
    except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
        return None
    try:
        profile_id = int(request.POST['checkedTarget'])
        profile = Profile.objects.get(id=profile_id)
    except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
        pass
    else:
        poll.target = profile
        poll.save()
    return poll


def _get_rendered_page_for_step_2(request: WSGIRequest, poll: Poll) -> dict:
    head_main = SimpleTemplateResponse('main/poll/select_target/select_target_head_main.html', {}).rendered_content
    head_move = SimpleTemplateResponse('main/poll/select_target/select_target_head_move.html', {}).rendered_content

    profile = get_user_profile(request)
    company: Company = profile.company
    profiles = company.profile_set.all()

    categories_args = {
        'participants': _build_team_profiles_list(profiles, company, [poll.target]),
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

    return {
        'pollId': poll.pk,
        'headMain': head_main,
        'headMove': head_move,
        'categories': categories
    }


def poll_preview(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        try:
            poll_id = int(request.POST['pollId'])
            poll = Poll.objects.get(id=poll_id)
            poll = _create_or_change_poll(request, poll)
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            poll = _create_or_change_poll(request, None)
        version = _create_new_questions_or_change(request, poll)
        poll.questions.all().exclude(version=version).delete()
        created_poll = _build_poll(poll)
        if poll.target is not None:
            created_poll['target'] = {
                'name': poll.target.name,
                'surname': poll.target.surname,
                'patronymic': poll.target.patronymic
            }
        content = SimpleTemplateResponse('main/poll/taking_poll_preview.html',
                                         {'poll': created_poll}).rendered_content
        return JsonResponse({'content': content, 'pollId': poll.pk}, status=200)


def poll_editor(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        try:
            poll_id = int(request.POST['pollId'])
            poll = Poll.objects.get(id=poll_id)
        except (MultiValueDictKeyError, ObjectDoesNotExist):
            return JsonResponse({}, status=400)
        created_poll = _build_poll(poll)
        content = SimpleTemplateResponse('main/poll/editor/content_poll_editor.html',
                                         {'poll': created_poll}).rendered_content
        return JsonResponse({'content': content}, status=200)


def cancel_created_poll(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        try:
            poll = Poll.objects.get(id=int(request.POST['pollId']))
            poll = _create_or_change_poll(request, poll)
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            return JsonResponse({}, status=200)
        else:
            poll.delete()
            return JsonResponse({}, status=200)


def send_poll(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        # todo
        poll = _save_information_from_step_3(request)
        if poll is None:
            return JsonResponse({}, status=400)

        poll.is_submitted = True
        poll.save()
        create_unique_key(poll)

        profile = get_user_profile(request)
        created_poll = CreatedPoll()
        created_poll.poll = poll
        created_poll.profile = profile
        created_poll.save()

        sending_emails(request, poll)
        return JsonResponse({}, status=200)


def create_unique_key(poll: Poll):
    poll_id_changed = poll.pk % 1000 + 1000
    initiator_id_changed = poll.initiator.id % 1000 + 1000
    target_id_changed = poll.initiator.id % 1000 + 1000
    creation_date: datetime = poll.creation_date
    key = '{}{}{}{}'.format(poll_id_changed, initiator_id_changed, target_id_changed, creation_date)
    poll.key = key
    poll.save()


def sending_emails(request: WSGIRequest, poll: Poll):
    # todo
    mail_subject = 'Новый опрос'
    link = "{}://{}".format(request._get_scheme(), request.get_host()) + '/compiling_poll_link/{}/'.format(poll.key)
    message = render_to_string('main/taking_poll_notifications_email.html', {
        'target': {
            'name': poll.target.name,
            'surname': poll.target.surname
        },
        'link': link
    })
    email = EmailMessage(
        mail_subject, message, to=[i.profile.user.email for i in NeedPassPoll.objects.filter(poll=poll)]
    )
    email.send()


def render_category_teams_on_step_3(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        poll = _save_information_from_step_3(request)
        if poll is None:
            return JsonResponse({}, status=400)
        profile = get_user_profile(request)
        company = profile.company
        if SurveyWizard.objects.filter(profile=profile).exists():
            teams = company.group_set.all()
        else:
            teams = profile.groups.all()
        args = {
            'teams': _build_team_list(teams, [i.profile for i in NeedPassPoll.objects.filter(poll=poll)], profile)
        }
        content = SimpleTemplateResponse('main/poll/select_interviewed/content_teams.html',
                                         args).rendered_content
        return JsonResponse({'content': content}, status=200)


def render_category_participants_on_step_3(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        poll = _save_information_from_step_3(request)
        if poll is None:
            return JsonResponse({}, status=400)
        profile = get_user_profile(request)
        company = profile.company
        profiles = company.profile_set.all().exclude(pk=profile.pk)
        args = {'participants': _build_team_profiles_list(profiles, company,
                                                          [i.profile for i in NeedPassPoll.objects.filter(poll=poll)])}
        content = SimpleTemplateResponse('main/poll/select_interviewed/content_participants.html',
                                         args).rendered_content
        return JsonResponse({'content': content}, status=200)


def search_step_3(request: WSGIRequest, template_id) -> JsonResponse:
    # todo fix bug (коряво работает поиск на русском, находит инициатора опроса)
    if request.is_ajax():
        try:
            poll_id = int(request.POST['pollId'])
            poll = Poll.objects.get(id=poll_id)
        except (ValueError, ObjectDoesNotExist, MultiValueDictKeyError):
            return JsonResponse({}, status=400)
        mode = request.POST['mode']
        user_input: str = request.POST['input']
        profile = get_user_profile(request)
        result_search = _search(mode, user_input, profile)

        if mode == 'participants':
            content_participants_args = {
                'participants': _build_team_profiles_list(
                    result_search, profile.company, [i.profile for i in NeedPassPoll.objects.filter(poll=poll)])
            }
            content = SimpleTemplateResponse('main/poll/select_interviewed/content_participants.html',
                                             content_participants_args).rendered_content
        elif mode == 'teams':
            collected_teams = _build_team_list(result_search,
                                               [i.profile for i in NeedPassPoll.objects.filter(poll=poll)])
            content_teams_args = {
                'teams': collected_teams
            }
            content = SimpleTemplateResponse('main/poll/select_interviewed/content_teams.html',
                                             content_teams_args).rendered_content
        else:
            return JsonResponse({}, status=400)
        return JsonResponse({'content': content}, status=200)
