import uuid

from django.shortcuts import redirect
from django.shortcuts import render

from main.forms import TeamForm
from main.models import Group
from main.views.auxiliary_general_methods import *


def create_team(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {
        'title': 'Создание новой группы',
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
        return redirect('/communications/')
    return render(request, 'main/add_new_team.html', args)


def connect_to_team_to_key(request):
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
                return render(request, 'main/connect_to_team.html', args)
        except:
            args['error'] = "Ключ не существует или введен неверно"
            return render(request, 'main/connect_to_team.html', args)
        else:
            profile.groups.add(group)
            profile.save()
            return redirect('/communications/')
    return render(request, 'main/connect_to_team.html', args)


def connect_to_team_to_link(request, key):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {'title': 'Присоединиться к комманде'}
    profile = get_user_profile(request)

    try:
        group = Group.objects.get(key=key)
        if group in profile.groups.all():
            return redirect("/groups/{}/".format(group.id))
    except:
        return render(request, 'main/error_old.html', {
            'error': "Этой группы не существует или ссылка введена неправильно"
        })
    else:
        profile.groups.add(group)
        profile.save()
        return redirect("/groups/{}/".format(group.id))


def teams_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    teams = profile.groups.all()
    args = {
        'title': "Круги общения",
        'teams': teams,
        'profile': profile,
    }

    try:
        photo = profile.profilephoto.photo
        args['photo'] = photo
        args['photo_height'] = get_photo_height(photo.width, photo.height)
    except:
        args['photo'] = None

    return render(request, 'main/communications.html', args)


def team_user_view(request, group_id):
    args = {}

    if auth.get_user(request).is_anonymous:
        return redirect('/')
    try:
        group = Group.objects.get(id=group_id)
        profile = get_user_profile(request)
        if profile not in group.profile_set.all():
            raise Exception()
    except:
        #args['error'] = "Данной группы не существует"
        return redirect('/communications/')

    args['users'] = group.profile_set.all()

    if auth.get_user(request).id == group.owner.id:
        args['link_to_enter'] = request.scheme + "://" + request.get_host() + "/invite/t/" + group.key
    args['owner'] = {'pk': group.owner.profile.pk,
                     'name': group.owner.profile.name,
                     'surname': group.owner.profile.surname}
    args['team_name'] = group.name
    args['title'] = group.name
    return render(request, 'main/team_view.html', args)
