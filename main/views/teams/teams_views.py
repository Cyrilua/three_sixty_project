import uuid
from datetime import datetime

from main.forms import TeamForm
from main.models import Group, Moderator, PositionCompany, PlatformCompany, ProfilePhoto, SurveyWizard, Invitation
from ..auxiliary_general_methods import *
from ..company_views import _get_roles
from django.shortcuts import redirect, render
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.db.models import Q
from django.template.response import SimpleTemplateResponse
from django.contrib.sites.shortcuts import get_current_site


def teams_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    args = {
        'teams': _build_teams(profile.groups.all(), profile),
        'profile': get_header_profile(profile)
    }
    return render(request, 'main/teams/teams_view.html', args)


def _build_teams(teams: list, current_profile: Profile) -> list:
    result = []
    for team in teams:
        team: Group
        collected_team = {
            'id': team.pk,
            'href': '/team/{}/'.format(team.pk),
            'name': team.name,
            'description': team.description,
            'quantity': team.profile_set.all().count(),
            'i_am_leader': team.owner == current_profile
        }
        result.append(collected_team)
    return result


def create_team(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    new_group = Group()
    new_group.owner = profile
    new_group.name = 'Новая команда'
    new_group.description = 'Описание'
    new_group.company = profile.company
    new_group.save()
    _create_unique_key(new_group)

    profile.groups.add(new_group)
    return redirect('/team/{}/'.format(new_group.pk))


def _create_unique_key(team: Group):
    team_id_changed = team.pk % 1000 + 1000
    owner_id_changed = team.owner.pk % 1000 + 1000
    date_now = datetime.today()
    date_changed_str = '{}{}{}{}{}{}{}'.format(date_now.day, date_now.month,
                                               date_now.year, date_now.hour, date_now.minute, date_now.second, date_now.microsecond)
    key = '{}{}{}'.format(team_id_changed, owner_id_changed, date_changed_str)
    team.key = key
    team.save()


def search_teams(request: WSGIRequest) -> JsonResponse:
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)
        profile = get_user_profile(request)
        user_input = request.GET.get('search', '')
        teams = profile.groups.all()
        teams = get_search_result_for_teams(teams, user_input)
        collected_teams = _build_teams(teams, profile)
        content = SimpleTemplateResponse('main/teams/teams.html',
                                         {'teams': collected_teams}).rendered_content
        return JsonResponse({'content': content}, status=200)



