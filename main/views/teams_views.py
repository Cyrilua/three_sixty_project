import uuid

from main.forms import TeamForm
from main.models import Group
from .auxiliary_general_methods import *
from . import auxiliary_general_methods
from django.shortcuts import redirect, render

from django.http import JsonResponse


def team_user_view(request, group_id: int) -> render:
    args = {}

    return render(request, 'main/teams/team_view.html', args)


def search_team_for_invite(request, profile_id: int) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    try:
        alien_profile = Profile.objects.get(id=profile_id)
    except:
        return redirect('/')
    alien_commands = alien_profile.groups.all()

    user = auth.get_user(request)
    profile = get_user_profile(request)
    commands = filter(lambda x: x not in alien_commands, profile.groups.all())
    #if not profile_is_owner(request):
    #    commands = filter(lambda x: x.owner.id == user.id, commands)
    args = {
        'title': "Пригласить в команду",
        'teams': build_teams(commands, profile_id)
    }
    return render(request, 'main/teams/search_team_for_invite_from_alien_profile.html', args)


def build_teams(commands: filter, alien_profile_id: int) -> list:
    result = []
    for team in commands:
        users = team.profile_set.all()
        collected_team = {
            'name': team.name,
            'about': team.description,
            'members': len(users),
            'url': '/team/{}/'.format(team.id),
            'url_send_invite': '/{}/invite/{}/'.format(alien_profile_id, team.id)
        }
        result.append(collected_team)
    return result


def teams_view(request):
    args = {}
    return render(request, 'main/teams/teams_view.html', args)


def team_setting(request, team_id):
    args = {}
    return render(request, 'main/teams/team_setting.html', args)


def team_new_invites(request, team_id):
    args = {}
    return render(request, 'main/teams/team_new_invites.html', args)
