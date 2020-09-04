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
    photo = profile.profilephoto.photo

    profile_data = _build_profile_data(auth.get_user(request), get_user_profile(request))

    args = {
        "title": "Главная",
        'photo': photo,
        'profile': profile_data[0],
        'roles': profile_data[1],
        'data': {
            'new': {
                'polls': NeedPassPoll.objects.filter(profile=profile, is_viewed=False).count(),
                'results': CreatedPoll.objects.filter(profile=profile, is_viewed=False, poll__count_passed__gt=2).count(),
                'invites': Invitation.objects.filter(profile=profile, is_viewed=False).count()
            }
        }
    }
    args['profile']['photo'] = photo
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
            return JsonResponse({}, status=404)

        selected_category = request.GET.get('selectedCategory', '')
        collected = _build_notifications(profile, selected_category)
        if collected is None:
            return JsonResponse({}, status=400)

        content = SimpleTemplateResponse('main/user/notifications.html',
                                         {'notifications': collected}).rendered_content
        return JsonResponse({'content': content}, status=200)


def _build_notifications(profile: Profile, selected_category: str):
    if selected_category == 'results':
        notifications = CreatedPoll.objects.filter(profile=profile, is_viewed=False).filter(poll__count_passed__gt=2)
        return _build_notifications_poll(notifications)

    elif selected_category == 'polls':
        result = _build_notifications_poll(NeedPassPoll.objects.filter(profile=profile))
        return result

    elif selected_category == 'invites':
        return _build_invites(profile)
    return None


def _build_notifications_poll(notifications_polls) -> list:
    result = []
    for notification in notifications_polls:
        notification: (CreatedPoll, NeedPassPoll)
        if type(notification) is CreatedPoll:
            type_notification = 'result'
            url = '/poll/result/{}/'.format(notification.poll.pk)
        else:
            url = '/poll/compiling_poll/{}/'.format(notification.poll.pk)
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
    notifications_polls.update(is_rendered=True)
    return result


def _build_invites(profile: Profile) -> list:
    result = []
    invitations = Invitation.objects.filter(profile=profile)
    for invite in invitations:
        invite: Invitation

        team = invite.team

        initiator: Profile = invite.initiator
        collected_notification = {
            'href': '/team/{}/invite/'.format(team.pk),
            'date': invite.date,
            'title': team.name,
            'more': {
                'name': "{} {} {}".format(initiator.surname, initiator.name, initiator.patronymic),
                'url': '/{}/'.format(initiator.pk)
            },
            'about': team.description,
            'is_viewed': invite.is_viewed,
            'is_new': not invite.is_rendered,
            'type': 'invite',
            'id': invite.pk,
        }
        result.append(collected_notification)
    invitations.update(is_rendered=True)
    return result


def new_notification(request: WSGIRequest, profile_id: int):
    if request.is_ajax():
        profile = get_user_profile(request)
        # todo забаговало
        #if profile.pk != profile_id:
        #    return JsonResponse({}, status=400)

        category = request.GET.get('category', '')

        if category == 'results':
            collected_notifications = _build_notifications_poll(
                CreatedPoll.objects.filter(profile=profile, is_viewed=False, is_rendered=False).filter(poll__count_passed__gt=2))

        elif category == 'polls':
            collected_notifications = _build_notifications_poll(
                NeedPassPoll.objects.filter(profile=profile, is_viewed=False, is_rendered=False))

        elif category == 'invites':
            collected_notifications = _build_invites(profile)

        else:
            return JsonResponse({}, status=400)

        count_new_my_poll = CreatedPoll.objects.filter(profile=profile, is_viewed=False, poll__count_passed__gt=2).count()
        count_new_polls = NeedPassPoll.objects.filter(profile=profile, is_viewed=False).count()
        count_new_invitations = Invitation.objects.filter(profile=profile, is_viewed=False).count()

        content = SimpleTemplateResponse('main/user/notifications.html',
                                         {'notifications': collected_notifications}).rendered_content
        args = {
            'notificationsCount':
                {
                    'polls': count_new_polls,
                    'results': count_new_my_poll,
                    'invites': count_new_invitations
                },
            'content': content
        }
        return JsonResponse(args, status=200)


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


def mark_notification_as_viewed(request: WSGIRequest, profile_id: int, notification_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        profile = get_user_profile(request)
        if profile.pk != profile_id:
            return JsonResponse({}, status=400)

        category = request.POST.get('category', '')
        if category == 'polls':
            notification = NeedPassPoll.objects.filter(id=notification_id)
        elif category == 'results':
            notification = CreatedPoll.objects.filter(id=notification_id)
        elif category == 'invites':
            notification = Invitation.objects.filter(id=notification_id)
        else:
            return JsonResponse({}, status=400)
        if notification.first() is None:
            return JsonResponse({}, status=400)
        notification.update(is_viewed=True)
        return JsonResponse({}, status=200)


def remove_invite(request: WSGIRequest, profile_id: int, notification_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        profile = get_user_profile(request)
        if profile.pk != profile_id:
            return JsonResponse({}, status=400)

        invite = Invitation.objects.filter(id=notification_id).first()
        if invite is None:
            return JsonResponse({}, status=404)
        invite.delete()
        return JsonResponse({}, status=200)
