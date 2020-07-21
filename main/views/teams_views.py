import uuid

from main.forms import TeamForm
from main.models import Group
from .auxiliary_general_methods import *
from . import notifications_views

from django.http import JsonResponse


def create_team(request) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {
        'title': 'Создание новой команды',
        'team_form': TeamForm()
    }

    user = auth.get_user(request)
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        team_form = TeamForm(request.POST)

        if team_form.is_valid():
            new_team = team_form.save(commit=False)
            new_team.owner = user
            new_team.key = uuid.uuid4().__str__()
            new_team.save()

            profile.groups.add(new_team)
            profile.groups.add()
        return redirect('/')
    return render(request, 'main/teams/old/add_new_team.html', args)


def connect_to_team_to_key(request) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {'title': 'Присоединиться к комманде'}
    profile = get_user_profile(request)

    if request.method == "POST":
        try:
            key_group = request.POST.get('key', '')
            group = Group.objects.get(key=key_group)
            if group in profile.groups.all():
                args['error'] = "Пользователь уже состоит в этой команде"
                return render(request, 'main/teams/old/connect_to_team.html', args)
        except:
            args['error'] = "Ключ не существует или введен неверно"
            return render(request, 'main/teams/old/connect_to_team.html', args)
        else:
            profile.groups.add(group)
            profile.save()
            return redirect('/')
    return render(request, 'main/teams/old/connect_to_team.html', args)


def connect_to_team_to_link(request, key: str) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)

    try:
        group = Group.objects.get(key=key)
        if group in profile.groups.all():
            return redirect("/team/{}/".format(group.id))
    except:
        return redirect('/')
    else:
        profile.groups.add(group)
        profile.save()
        return redirect("/team/{}/".format(group.id))


def team_user_view(request, group_id: int) -> render:
    args = {}

    if auth.get_user(request).is_anonymous:
        return redirect('/')
    try:
        group = Group.objects.get(id=group_id)
        profile = get_user_profile(request)
        if profile not in group.profile_set.all():
            raise Exception()
    except:
        return redirect('/')

    args['users'] = group.profile_set.all()

    if auth.get_user(request).id == group.owner.id:
        args['link_to_enter'] = request.scheme + "://" + request.get_host() + "/invite/t/" + group.key
    args['owner'] = {'pk': group.owner.profile.pk,
                     'name': group.owner.profile.name,
                     'surname': group.owner.profile.surname}
    args['team_name'] = group.name
    args['title'] = group.name
    args['group_id'] = group_id
    return render(request, 'main/teams/old/team_view.html', args)


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
    if not profile_is_owner(request):
        commands = filter(lambda x: x.owner.id == user.id, commands)
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


def send_notification_profile(request, profile_id: int, team_id: int) -> JsonResponse:
    try:
        alien_profile = Profile.objects.get(id=profile_id)
        command = Group.objects.get(id=team_id)
    except:
        return JsonResponse({}, status=400)

    profile = get_user_profile(request)

    notifications_views.create_notifications(profile=alien_profile,
                                             name=command.name,
                                             type_notification='invite_command',
                                             key=command.key,
                                             from_profile=profile)

    return JsonResponse({}, status=200)
