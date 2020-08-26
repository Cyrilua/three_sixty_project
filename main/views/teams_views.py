import uuid

from main.forms import TeamForm
from main.models import Group
from .auxiliary_general_methods import *
from .company_views import _get_roles
from django.shortcuts import redirect, render

from django.http import JsonResponse


def team_view(request, group_id: int) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    team: Group = Group.objects.filter(id=group_id).first()
    if team is None:
        return render(request, 'main/errors/global_error.html', {'global_error': 404})
    profile = get_user_profile(request)
    args = {
        'team': {
            'id': team.pk,
            'name': team.name,
            'description': team.description,
        },
        'is_leader': profile == team.owner,
        'teammates': _build_teammates(team.profile_set.all(), team, profile),
        'profile': get_header_profile(profile)
    }
    company = team.company
    if company is not None:
        args['company'] = {
            'href': '/company/{}/'.format(company.pk),
            'name': company.name,
        }
    print(args)
    return render(request, 'main/teams/team_view.html', args)


def _build_teammates(teammates: list, team: Group, current_profile: Profile) -> list:
    result = []
    for teammate in teammates:
        teammate: Profile
        try:
            photo = teammate.profilephoto.photo
        except ObjectDoesNotExist:
            photo = None
        collected_teammate = {
            'id': teammate.pk,
            'photo': photo,
            'href': '/{}/'.format(teammate.pk),
            'surname': teammate.surname,
            'name': teammate.name,
            'patronymic': teammate.patronymic,
            'roles': _get_roles(teammate),
            'is_leader': team.owner == teammate,
            'positions': teammate.positions.all(),
            'platforms': teammate.platforms.all(),
            'is_my_profile': teammate == current_profile
        }
        result.append(collected_teammate)
    return result


def team_settings_view(request, group_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    team: Group = Group.objects.filter(id=group_id).first()
    if team is None:
        return redirect('/')
    args = {
        'team': {
            'name': team.name,
            'description': team.description,
            'hrefForInvite': '',  # todo,
        }
    }
    return render(request, 'main/teams/team_setting.html', args)


def team_remove(request, group_id):
    pass


def search_team_for_invite(request, profile_id: int) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    alien_profile = Profile.objects.filter(id=profile_id).first
    if alien_profile is None:
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


def team_setting(request, team_id):
    args = {}
    return render(request, 'main/teams/team_setting.html', args)


def team_new_invites(request, team_id):
    args = {}
    return render(request, 'main/teams/team_new_invites.html', args)


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

    profile.groups.add(new_group)
    return redirect('/team/{}/'.format(new_group.pk))
