from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.template.response import SimpleTemplateResponse
from django.utils.datastructures import MultiValueDictKeyError

from main.models import Poll, Group, SurveyWizard, Company, \
    NeedPassPoll
from main.views.auxiliary_general_methods import *
from .choose_target import build_profile


def save_information(request: WSGIRequest) -> Poll:
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
    # todo удаляются пользователи, которые не состоят в ккакой-либо команде
    profiles_for_delete = NeedPassPoll.objects.filter(poll=poll).exclude(version=version)
    profiles_for_delete.delete()
    return poll


def get_rendered_page(request: WSGIRequest, poll: Poll) -> dict:
    args = {}
    profile = get_user_profile(request)
    if SurveyWizard.objects.filter(profile=profile).exists():
        args['is_master'] = 'is_master'
    main = SimpleTemplateResponse('main/poll/select_interviewed/select_interviewed_head_main.html',
                                  args).rendered_content
    move = SimpleTemplateResponse('main/poll/select_interviewed/select_interviewed_head_move.html',
                                  args).rendered_content
    # todo fix (сделать что то с пользователями без компании)
    company = profile.company
    target_id = -1 if poll.target is None else poll.target.id
    initiator_id = -1 if poll.initiator is None else poll.initiator.id
    profiles = Profile.objects.filter(company=company).exclude(id=target_id).exclude(id=initiator_id)

    categories_args = {
        'participants': _build_team_profiles_list(profiles, company, NeedPassPoll.objects.filter(poll=poll), profile),
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


def _build_team_list(teams: (list, filter), checked_profiles: QuerySet, unbilding_user: Profile) -> list:
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


def _build_team_profiles_list(profiles: (list, filter), group: (Group, Company), checked_profiles: QuerySet,
                              unbilding_user: Profile) -> list:
    result = []
    for profile in profiles:
        if profile == unbilding_user:
            continue
        profile: Profile
        collected_profile = build_profile(profile)
        collected_profile['is_checked'] = checked_profiles.filter(profile=profile).exists()
        if group is not None:
            collected_profile['is_leader'] = group.owner == profile

        result.append(collected_profile)

    return result


def render_category_teams_on_step_3(request: WSGIRequest) -> JsonResponse:
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
        'teams': _build_team_list(teams, NeedPassPoll.objects.filter(poll=poll), profile)
    }
    content = SimpleTemplateResponse('main/poll/select_interviewed/content_teams.html',
                                     args).rendered_content
    return JsonResponse({'content': content}, status=200)


def render_category_participants_on_step_3(request: WSGIRequest) -> JsonResponse:
    poll = save_information(request)
    if poll is None:
        return JsonResponse({}, status=400)
    profile = get_user_profile(request)
    company = profile.company
    profiles = company.profile_set.all().exclude(pk=profile.pk)
    args = {'participants': _build_team_profiles_list(profiles, company,
                                                      NeedPassPoll.objects.filter(poll=poll), profile)}
    content = SimpleTemplateResponse('main/poll/select_interviewed/content_participants.html',
                                     args).rendered_content
    return JsonResponse({'content': content}, status=200)


def search_step_3(request: WSGIRequest) -> JsonResponse:
    try:
        poll_id = int(request.POST['pollId'])
        poll = Poll.objects.get(id=poll_id)
    except (ValueError, ObjectDoesNotExist, MultiValueDictKeyError):
        return JsonResponse({}, status=400)
    mode = request.POST['mode']
    user_input: str = request.POST['input']
    profile = get_user_profile(request)
    company = profile.company
    if mode == 'participants':
        result_search = get_search_result_for_profiles(company.profile_set.all(), user_input.split(), company)
        content_participants_args = {
            'participants': _build_team_profiles_list(result_search, profile.company,
                                                      NeedPassPoll.objects.filter(poll=poll),
                                                      unbilding_user=profile)
        }
        content = SimpleTemplateResponse('main/poll/select_interviewed/content_participants.html',
                                         content_participants_args).rendered_content
    elif mode == 'teams':
        user_is_master = SurveyWizard.objects.filter(profile=profile).exists()
        if user_is_master:
            teams: QuerySet = Group.objects.filter(company=profile.company)
        else:
            teams: QuerySet = profile.groups.all()
        result_search = get_search_result_for_teams(teams, user_input)
        collected_teams = _build_team_list(result_search, NeedPassPoll.objects.filter(poll=poll),
                                           unbilding_user=profile)
        content_teams_args = {
            'teams': collected_teams
        }
        content = SimpleTemplateResponse('main/poll/select_interviewed/content_teams.html',
                                         content_teams_args).rendered_content
    else:
        return JsonResponse({}, status=400)
    return JsonResponse({'content': content}, status=200)
