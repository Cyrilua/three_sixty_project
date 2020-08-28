import datetime

from django.template.response import SimpleTemplateResponse
from main.models import BirthDate, SurveyWizard, Moderator, NeedPassPoll, CreatedPoll, Invitation, Poll, Group, Company
from main.views.auxiliary_general_methods import *
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse


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
        'notifications': _build_notifications_poll(NeedPassPoll.objects.filter(profile=profile))
    }
    return render(request, 'main/user/profile.html', args)


def _build_profile_data(user, profile):
    profile_data = {
            'id': profile.id,
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
            'id': company.id,
            'url': '/company_view/{}/'.format(company.id),
            'name': company.name,
        }

        profile_data['platforms'] = profile.platforms.all()
        profile_data['positions'] = profile.positions.all()

    birth_date = BirthDate.objects.filter(profile=profile).first()
    if birth_date is not None:
        profile_data['birthdate'] = birth_date.birthday

    profile_data['email'] = user.email
    return [profile_data, roles]


def _get_user_roles(user, profile, company):
    roles = []
    if company is not None and company.owner.id == user.id:
        roles.append('boss')

    if SurveyWizard.objects.filter(profile=profile).exists():
        roles.append('master')

    if Moderator.objects.filter(profile=profile).exists():
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


def loading(request: WSGIRequest, profile_id: int) -> JsonResponse:
    if request.is_ajax():
        profile = get_user_profile(request)
        if profile != Profile.objects.filter(id=profile_id).first():
            return JsonResponse({}, 404)

        selected_category = request.GET.get('selectedCategory', '')
        print(selected_category)
        collected = _build_notifications(profile, selected_category)
        if collected is None:
            return JsonResponse({}, status=400)

        content = SimpleTemplateResponse('main/user/notifications.html',
                                         {'notifications': collected}).rendered_content
        return JsonResponse({'content': content})


def _build_notifications(profile: Profile, selected_category: str):
    if selected_category == 'results':
        return _build_notifications_poll(CreatedPoll.objects.filter(profile=profile))

    elif selected_category == 'polls':
        return _build_notifications_poll(NeedPassPoll.objects.filter(profile=profile))

    elif selected_category == 'invites':
        return _build_invites(profile)
    return None


def _build_notifications_poll(notifications_polls: list) -> list:
    result = []
    for notification in notifications_polls:
        notification: (CreatedPoll, NeedPassPoll)
        if type(notification) is CreatedPoll:
            type_notification = 'result'
            url = '/poll/result/{}/'.format(notification.poll.pk)
        else:
            url = '/compiling_poll/{}/'.format(notification.poll.pk)
            type_notification = 'poll'
        poll: Poll = notification.poll
        target_poll: Profile = poll.target
        collected_notification = {
            'title': poll.name_poll,
            'more': {
                'url': '/{}/'.format(target_poll.pk),
                'name': '{} {} {}'.format(target_poll.surname, target_poll.name, target_poll.patronymic)
            },
            'about': poll.description,
            'date': poll.creation_date,
            'href': url,
            'is_viewed': notification.is_viewed,
            'type': type_notification,
            'id': notification.id,
        }
        result.append(collected_notification)
    return result


def _build_invites(profile: Profile) -> list:
    result = []
    for invite in Invitation.objects.filter(profile=profile):
        invite: Invitation

        if invite.type == 'team':
            group = Group.objects.filter(pk=invite.invitation_group_id).first()
            watch_url = '/team/{}/'.format(group.pk)
        elif invite.type == 'company':
            group = Company.objects.filter(pk=invite.invitation_group_id).first()
            watch_url = 'company/{}/'.format(group.pk)
        else:
            continue
        if group is None:
            continue

        initiator: Profile = invite.initiator
        collected_notification = {
            'url': '',  # todo присоединение к объединению
            'date': invite.date,
            'title': {
                'name': group.name,
                'url': watch_url,
            },
            'more': {
                'name': "{} {} {}".format(initiator.surname, initiator.name, initiator.patronymic),
                'url': '/{}/'.format(initiator.pk)
            },
            'about': group.description,
            'complited': True  # todo
        }
        yield collected_notification
        #result.append(collected_notification)
    #return result


def get_other_profile_render(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    try:
        photo = profile.profilephoto.photo
    except ObjectDoesNotExist:
        photo = None

    current_profile = get_user_profile(request)
    profile_data = _build_profile_data(profile.user, profile)

    args = {
        "title": "Просмотр профиля пользователя",
        'profile': get_header_profile(current_profile),
        'photo': photo,
        'alien_profile': profile_data[0],
        'roles': profile_data[1],
    }
    return render(request, "main/user/alien_profile.html", args)
