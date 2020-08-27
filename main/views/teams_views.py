import uuid
from datetime import datetime

from main.forms import TeamForm
from main.models import Group, Moderator, PositionCompany, PlatformCompany, ProfilePhoto, SurveyWizard, Invitation
from .auxiliary_general_methods import *
from .company_views import _get_roles
from django.shortcuts import redirect, render
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.db.models import Q
from django.template.response import SimpleTemplateResponse
from django.contrib.sites.shortcuts import get_current_site


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
        'profile': get_header_profile(profile),
        'teammates': _build_teammates(team.profile_set.all(), team, profile),
    }
    company = team.company
    if company is not None:
        args['company'] = {
            'href': '/company/{}/'.format(company.pk),
            'name': company.name,
        }
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
            'is_my_profile': teammate == current_profile,
            'is_in_team': team.profile_set.filter(id=teammate.pk).exists()
        }
        result.append(collected_teammate)
    return result


def team_settings_view(request, group_id):
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
            'hrefForInvite': ''.join(['http://', get_current_site(request).domain, '/team/{}/'.format(team.pk),
                                      'invite_team/', team.key])
        },
        'is_leader': profile == team.owner,
        'profile': get_header_profile(profile),
    }
    return render(request, 'main/teams/team_setting.html', args)


def team_remove(request, group_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    team: Group = Group.objects.filter(id=group_id).first()
    if team is None:
        return render(request, 'main/errors/global_error.html', {'global_error': 404})

    profile = get_user_profile(request)
    if team.owner != profile or not _profile_is_owner_or_moderator(profile):
        return render(request, 'main/errors/global_error.html', {'global_error': 403})
    team.delete()
    return redirect('/teams/')


def _profile_is_owner_or_moderator(profile: Profile):
    company = profile.company
    is_owner = False
    if company is not None:
        is_owner = company.owner == profile
    return Moderator.objects.filter(profile=profile).exists() or is_owner


def team_change(request: WSGIRequest, group_id: int) -> redirect:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        team: Group = Group.objects.filter(id=group_id).first()
        if team is None:
            return JsonResponse({}, status=404)

        profile = get_user_profile(request)
        if team.owner != profile or not _profile_is_owner_or_moderator(profile):
            return JsonResponse({}, status=403)

        team.name = request.POST.get('name', team.name)
        team.description = request.POST.get('description', team.description)
        team.save()
        return JsonResponse({}, status=200)


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


def team_new_invites(request, group_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    team = Group.objects.filter(id=group_id).first()
    if team is None:
        return render(request, 'main/errors/global_error.html', {'global_error': 404})
    profile = get_user_profile(request)
    company = profile.company
    args = {
        'users': _build_teammates(company.profile_set.all(), team, profile),
        'profile': get_header_profile(profile)
    }
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


def search_teammate(request: WSGIRequest, group_id: int) -> JsonResponse:
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)
        team = Group.objects.filter(id=group_id).first()
        if team is None:
            return JsonResponse({}, status=404)
        profile = get_user_profile(request)
        user_input = request.GET.get('search', '').split()
        profiles = get_search_result_for_profiles(team.profile_set.all(), user_input, profile.company)
        completed_profiles = _build_teammates(profiles, team, profile)
        content = SimpleTemplateResponse('main/teams/teammates.html',
                                         {'teammates': completed_profiles}).rendered_content
        return JsonResponse({'content': content}, status=200)


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


def join_using_link(request, group_id, key: str):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    team = Group.objects.filter(id=group_id).first()
    if team is None:
        return render(request, 'main/errors/global_error.html', {'global_error': 404})
    if team.key != key:
        return render(request, 'main/errors/global_error.html', {'global_error': 404})
    profile = get_user_profile(request)
    profile.groups.add(team)
    return redirect('/team/{}/'.format(team.pk))


def join_user_from_page(request: WSGIRequest, group_id: int, profile_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=400)

        team = Group.objects.filter(id=group_id).first()
        if team is None:
            return JsonResponse({}, status=400)

        profile_added = Profile.objects.filter(id=profile_id).first()
        if profile_added is None:
            return JsonResponse({}, status=400)

        current_profile = get_user_profile(request)
        if team.owner != current_profile or not _profile_is_owner_or_moderator(current_profile):
            return JsonResponse({}, status=403)
        new_invitation, created = Invitation.objects.get_or_create(profile_id=profile_id, invitation_group_id=group_id)
        new_invitation: Invitation
        if created:
            new_invitation.type = 'team'
            new_invitation.profile = profile_added
            new_invitation.initiator = current_profile
            new_invitation.invitation_group_id = group_id
        new_invitation.date = date.today()
        new_invitation.is_viewed = False
        new_invitation.is_rendered = False
        new_invitation.save()
        return JsonResponse({}, status=200)
