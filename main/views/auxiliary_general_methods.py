from django.contrib import auth
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import User

from main.models import Profile, CompanyHR


def get_user_profile(request):
    user = auth.get_user(request)
    return Profile.objects.get(user=user)


def get_photo_height(width, height):
    result = round(177 / (width / height))
    if result > 300:
        result = 300
    return result


def find_target(request, poll_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {
        'title': "Поиск цели опроса",

    }
    if poll_id != -1:
        args['poll_id'] = poll_id
    if not user_is_hr_or_owner:
        args['error'] = "У пользователя нет доступа для этой операции"
        return render(request, 'main/search_profile.html', args)

    if request.method == "POST":
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')
        patronymic = request.POST.get('patronymic', '')
        position = request.POST.get('position', '')
        platform = request.POST.get('platform', '')

        profiles = None
        if valid_input(name):
            profiles = Profile.objects.filter(name=name)
        if valid_input(surname):
            profiles = filter_profile(lambda x: x.surname == surname, profiles)
        if valid_input(patronymic):
            profiles = filter_profile(lambda x: x.patronymic == patronymic, profiles)
        if valid_input(position):
            profiles = filter_profile(lambda x: x.position == position, profiles)
        if valid_input(platform):
            profiles = filter_profile(lambda x: x.platform == platform, profiles)
        args['profiles'] = []
        args['name'] = name
        args['surname'] = surname
        args['patronymic'] = patronymic
        args['position'] = position
        args['platform'] = platform
        for profile in profiles:
            args['profiles'].append({
                'surname': profile.surname,
                'name': profile.name,
                'patronymic': profile.patronymic,
                'url': '/target_poll/{}/{}/'.format(profile.id, poll_id)
            })
        args['poll_id'] = 0,
        return render(request, 'main/search_profile.html', args)

    return render(request, 'main/search_profile.html', args)


def user_is_hr_or_owner(request):
    user = auth.get_user(request)
    profile = get_user_profile(request)
    try:
        user_is_hr = CompanyHR.objects.get(profile=profile) is not None
    except:
        user_is_hr = False
    user_is_owner = profile.company.owner.id == user.id
    return user_is_owner or user_is_hr


def find_user(request,
              action_with_selected_user='main:profile',
              poll_id=-1,
              html_file='main/search_profile.html',
              title="Поиск пользователей",
              limited_access=False,
              function_determining_access=None):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {
        'title': title,
        'redirect': action_with_selected_user,
    }
    if poll_id != -1:
        args['poll_id'] = poll_id
    if limited_access:
        if not function_determining_access(request):
            args['error'] = "У пользователя нет доступа для этой операции"
            return render(request, html_file, args)

    if request.method == "POST":
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')
        patronymic = request.POST.get('patronymic', '')
        position = request.POST.get('position', '')
        platform = request.POST.get('platform', '')

        profiles = None
        if valid_input(name):
            profiles = Profile.objects.filter(name=name)
        if valid_input(surname):
            profiles = filter_profile(lambda x: x.surname == surname, profiles)
        if valid_input(patronymic):
            profiles = filter_profile(lambda x: x.patronymic == patronymic, profiles)
        if valid_input(position):
            profiles = filter_profile(lambda x: x.position == position, profiles)
        if valid_input(platform):
            profiles = filter_profile(lambda x: x.platform == platform, profiles)
        args['profiles'] = profiles
        args['name'] = name
        args['surname'] = surname
        args['patronymic'] = patronymic
        args['position'] = position
        args['platform'] = platform
        return render(request, html_file, args)

    return render(request, html_file, args)


def valid_input(user_input: str):
    return user_input is not None and user_input != ''


def filter_profile(func, profiles):
    if profiles is None:
        return filter(func, Profile.objects.all())
    return filter(func, profiles)
