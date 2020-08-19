import datetime

from main.models import BirthDate, SurveyWizard, Moderator, NeedPassPoll, CreatedPoll, Invitation, Poll, Group, Company
from main.views.auxiliary_general_methods import *
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist


def profile_view(request, profile_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if profile_id == get_user_profile(request).id or profile_id == -1:
        return get_render_user_profile(request)
    return get_other_profile_render(request, profile_id)


def get_render_user_profile(request):
    profile = get_user_profile(request)
    try:
        photo = profile.profilephoto.photo
    except ObjectDoesNotExist:
        photo = None

    profile_data = _build_profile_data(auth.get_user(request), get_user_profile(request))

    args = {
        "title": "Главная",
        'photo': photo,
        'profile': profile_data[0],
        'roles': profile_data[1],
        'notifications': _build_notifications(profile)
    }
    return render(request, 'main/user/profile.html', args)


def _build_profile_data(user, profile):
    profile_data = {
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic,
            'teams': _get_user_teams(profile)
        }

    company = profile.company
    roles = []
    if company is not None:
        roles = _get_user_roles(user, profile, company)
        profile_data['company'] = {
            'url': '/company_view/{}/'.format(company.id),
            'name': company.name,
        }

        profile_data['platforms'] = profile.platforms.all()
        profile_data['positions'] = profile.positions.all()

    try:
        profile_data['birthdate'] = BirthDate.objects.get(profile=profile).birthday
    except ObjectDoesNotExist:
        pass

    try:
        profile_data['email'] = user.email
    except ObjectDoesNotExist:
        pass
    return [profile_data, roles]


def _get_user_roles(user, profile, company):
    roles = []
    if company is not None and company.owner.id == user.id:
        roles.append('boss')
    try:
        SurveyWizard.objects.get(profile=profile)
    except ObjectDoesNotExist:
        pass
    else:
        roles.append('master')

    try:
        Moderator.objects.get(profile=profile)
    except ObjectDoesNotExist:
        pass
    else:
        roles.append('moderator')
    return roles


def _get_user_teams(profile):
    teams = []
    for team in profile.groups.all():
        teams.append({
            'url': '/team/{}/'.format(team.id),
            'name': team.name
        })
    return teams


def _build_notifications(profile: Profile) -> dict:
    return {
        'polls': _build_alien_polls(profile),
        'my_polls': _build_my_polls(profile),
        'invites': _invites
    }


def _build_alien_polls(profile: Profile) -> list:
    result = []
    for need_pass in NeedPassPoll.objects.filter(profile=profile):
        poll_need_pass: Poll = need_pass.poll
        result.append(_build_poll(poll_need_pass, True))
    return result


def _build_my_polls(profile: Profile) -> list:
    result = []
    for created_poll in CreatedPoll.objects.filter(profile=profile):
        result.append(_build_poll(created_poll.poll, False))
    return result


def _build_poll(poll: Poll, is_alien_polls: bool) -> dict:
    target_poll: Profile = poll.target
    collected_poll = {
        'title': poll.name_poll,
        'more': {
            'url': '/{}/'.format(target_poll.pk),
            'name': '{} {} {}'.format(target_poll.surname, target_poll.name, target_poll.patronymic)
        },
        'about': poll.description,
        'date': poll.creation_date,
        'complited': False,  # todo
        'url': '' if is_alien_polls else '',  # todo
    }
    return collected_poll


def _invites(profile: Profile) -> list:
    result = []
    for invite in Invitation.objects.filter(profile=profile):
        invite: Invitation
        group: (Group, Company) = None
        if invite.type == 'team':
            try:
                group = Group.objects.get(pk=invite.invitation_group_id)
            except ObjectDoesNotExist:
                continue
        elif invite.type == 'company':
            try:
                group = Company.objects.get(pk=invite.invitation_group_id)
            except ObjectDoesNotExist:
                continue
        else:
            continue
        initiator: Profile = invite.initiator
        collected_notification = {
            'url': '',  # todo присоединение к объединению
            'date': invite.date,
            'title': {
                'name': group.name,
                'url': '',  # todo просмотр страницы объединения
            },
            'more': {
                'name': "{} {} {}".format(initiator.surname, initiator.name, initiator.patronymic),
                'url': '/{}/'.format(initiator.pk)
            },
            'about': group.description,
            'complited': True  # todo
        }
        result.append(collected_notification)
    return result


def get_other_profile_render(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    try:
        photo = profile.profilephoto.photo
    except:
        photo = None

    profile_data = _build_profile_data(profile.user, profile)

    args = {
        "title": "Просмотр профиля пользователя",
        'photo': photo,
        'alien_profile': profile_data[0],
        'roles': profile_data[1],
    }
    return render(request, "main/user/alien_profile.html", args)
