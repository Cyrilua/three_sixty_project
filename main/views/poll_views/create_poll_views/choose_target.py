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


def get_rendered_page(request: WSGIRequest, poll: Poll) -> dict:
    head_main = SimpleTemplateResponse('main/poll/select_target/select_target_head_main.html', {}).rendered_content
    head_move = SimpleTemplateResponse('main/poll/select_target/select_target_head_move.html', {}).rendered_content

    profile = get_user_profile(request)
    company: Company = profile.company
    profiles = get_possible_respondents(poll, company)

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

    return {
        'pollId': poll.pk,
        'headMain': head_main,
        'headMove': head_move,
        'categories': categories
    }


def render_category_teams_on_step_2(request: WSGIRequest) -> JsonResponse:
    poll = save_information(request)
    if poll is None:
        return JsonResponse({}, status=400)
    profile = get_user_profile(request)
    company = profile.company
    if SurveyWizard.objects.filter(profile=profile).exists():
        teams = company.group_set.all()
    else:
        teams = profile.groups.all()
    args = {
        'teams': _build_team_list(teams, poll.target)
    }
    content = SimpleTemplateResponse('main/poll/select_target/content_teams.html',
                                     args).rendered_content
    return JsonResponse({'content': content}, status=200)


def render_category_participants_on_step_2(request: WSGIRequest) -> JsonResponse:
    poll = save_information(request)
    if poll is None:
        return JsonResponse({}, status=400)
    profile = get_user_profile(request)
    company = profile.company
    profiles = get_possible_respondents(poll, company)
    args = {'participants': _build_team_profiles_list(profiles, company, poll.target)}
    content = SimpleTemplateResponse('main/poll/select_target/content_participants.html',
                                     args).rendered_content
    return JsonResponse({'content': content}, status=200)


def _build_team_list(teams: (list, filter), checked_profile: Profile) -> list:
    result = []
    for team in teams:
        team: Group
        profiles = team.profile_set.all()
        collected_poll = {
            'id': team.pk,
            'name': team.name,
            'numbers': profiles.count(),
            'descriptions': team.description,
            'participants': _build_team_profiles_list(profiles, team, checked_profile),
            'href': ''
        }
        result.append(collected_poll)
    return result


def _build_team_profiles_list(profiles: (list, filter), group: (Group, Company), checked_profile: Profile) -> list:
    result = []
    for profile in profiles:
        collected_profile = build_profile(profile)
        collected_profile['is_checked'] = profile == checked_profile
        if group is not None:
            collected_profile['is_leader'] = group.owner == profile
        result.append(collected_profile)
    return result


def build_profile(profile) -> dict:
    try:
        photo = profile.profilephoto.photo
    except ObjectDoesNotExist:
        photo = None
    return {
        'href': '/{}/'.format(profile.pk),
        'id': profile.pk,
        'name': profile.name,
        'surname': profile.surname,
        'patronymic': profile.patronymic,
        'roles': _get_roles(profile),
        'positions': [i.name for i in profile.positions.all()],
        'platforms': [i.name for i in profile.platforms.all()],
        'photo': photo
    }


def _get_roles(profile: Profile) -> list:
    roles = []
    if profile.company is not None:
        if profile.company.owner.pk == profile.pk:
            roles.append('boss')
        if SurveyWizard.objects.filter(profile=profile).exists():
            roles.append('master')
        if Moderator.objects.filter(profile=profile).exists():
            roles.append('moderator')
    return roles


def search(request: WSGIRequest) -> JsonResponse:
    try:
        poll_id = int(request.POST['pollId'])
        poll = Poll.objects.get(id=poll_id)
        mode = request.POST['mode']
        user_input: str = request.POST['input']
    except (ValueError, ObjectDoesNotExist):
        return JsonResponse({}, status=400)

    profile = get_user_profile(request)
    company = profile.company
    checked_id = int(request.POST.get('checkedTarget', '-1'))
    profile_checked = Profile.objects.filter(id=checked_id).first()

    if mode == 'participants':
        profiles = get_possible_respondents(poll, company)
        start_from_company_or_polls = poll.start_from
        result_search = get_search_result_for_profiles(profiles, user_input.split(),
                                                       company if start_from_company_or_polls else None)
        content_participants_args = {
            'participants': _build_team_profiles_list(result_search, profile.company, profile_checked)
        }
        content = SimpleTemplateResponse('main/poll/select_target/content_participants.html',
                                         content_participants_args).rendered_content
    elif mode == 'teams':
        user_is_master = SurveyWizard.objects.filter(profile=profile).exists()
        if user_is_master:
            teams: QuerySet = Group.objects.filter(company=profile.company)
        else:
            teams: QuerySet = profile.groups.all()
        result_search = get_search_result_for_teams(teams, user_input)
        collected_teams = _build_team_list(result_search, profile_checked)
        content_teams_args = {
            'teams': collected_teams
        }
        content = SimpleTemplateResponse('main/poll/select_target/content_teams.html',
                                         content_teams_args).rendered_content
    else:
        return JsonResponse({}, status=400)
    return JsonResponse({'content': content}, status=200)


def save_information(request: WSGIRequest) -> Poll:
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


def get_possible_respondents(poll: Poll, company) -> QuerySet:
    if poll.start_from is None:
        return Profile.objects.filter(company=company)

    elif poll.start_from == 'team':
        team = Group.objects.filter(id=poll.from_id_group).first()
        profiles = team.profile_set.all()
        return profiles

    else:
        profiles = company.profile_set.all()
        return profiles
