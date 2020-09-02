from datetime import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect, render

from main.models import Group, Invitation
from ..auxiliary_general_methods import *


def teams_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    teams = _build_teams(profile.groups.all(), profile)
    args = {
        'teams': teams,
        'profile': get_header_profile(profile)
    }
    if len(teams) == 0:
        args['error'] = {
            'text': 'Вы не состоите ни в одной команде'
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
    new_group.description = 'Измение описание в настройках'
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
                                               date_now.year, date_now.hour, date_now.minute, date_now.second,
                                               date_now.microsecond)
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
        if len(collected_teams) == 0:
            content = get_render_bad_search('По вашему запросу ничего не найдено')
        else:
            content = SimpleTemplateResponse('main/teams/teams.html',
                                             {'teams': collected_teams}).rendered_content
        return JsonResponse({'content': content}, status=200)


def team_for_invite(request, profile_id: int) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    alien_profile = Profile.objects.filter(id=profile_id).first()
    if alien_profile is None:
        return render(request, 'main/errors/global_error.html', {'global_error': '404'})
    current_profile: Profile = get_user_profile(request)

    alien_commands = alien_profile.groups.all().values_list('id', flat=True)
    teams = current_profile.groups.all()
    args = {
        'title': "Пригласить в команду",
        'teams': build_teams(teams, alien_profile, alien_commands),
        'profile': get_header_profile(current_profile),
        'alien_profile': {
            'id': profile_id,
        }
    }
    return render(request, 'main/teams/search_team_for_invite_from_alien_profile.html', args)


def search_team_for_invite(request, profile_id: int) -> JsonResponse:
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)
        alien_profile = Profile.objects.filter(id=profile_id).first()
        if alien_profile is None:
            return JsonResponse({}, status=404)
        profile = get_user_profile(request)
        user_input = request.GET.get('search', '')
        teams = profile.groups.all()
        teams = get_search_result_for_teams(teams, user_input)
        alien_commands = alien_profile.groups.all().values_list('id', flat=True)
        collected_teams = build_teams(teams, profile, alien_commands)
        if len(collected_teams) == 0:
            content = get_render_bad_search('По вашему запросу ничего не найдено')
        else:
            content = SimpleTemplateResponse('main/teams/teams_for_invites.html',
                                             {'teams': collected_teams}).rendered_content
        return JsonResponse({'content': content}, status=200)


def build_teams(commands: filter, alien_profile: Profile, alien_commands) -> list:
    result = []
    for team in commands:
        users = team.profile_set.all()
        collected_team = {
            'id': team.pk,
            'name': team.name,
            'about': team.description,
            'members': len(users),
            'url': '/team/{}/'.format(team.id),
            'url_send_invite': '/{}/invite/{}/'.format(alien_profile.pk, team.id),
            'is_may_be_invited': not alien_commands.filter(id=team.pk).exists() and \
                                 not Invitation.objects.filter(team=team, profile=alien_profile).exists(),
        }
        result.append(collected_team)
    return result


def invite_to_team(request: WSGIRequest, profile_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        current_profile = get_user_profile(request)

        changed_profile_role = Profile.objects.filter(id=profile_id).first()
        if changed_profile_role is None:
            return JsonResponse({}, status=404)
        group_id = int(request.POST.get('teamId', '-1'))
        team = Group.objects.filter(id=group_id).first()
        if team is None:
            return JsonResponse({}, status=404)

        try:
            new_invitation = Invitation.objects.get(profile_id=profile_id, team=team)
        except ObjectDoesNotExist:
            new_invitation = Invitation()
        new_invitation.profile = changed_profile_role
        new_invitation.initiator = current_profile
        new_invitation.team = team
        new_invitation.date = date.today()
        new_invitation.is_viewed = False
        new_invitation.is_rendered = False
        new_invitation.save()
        return JsonResponse({}, status=200)
