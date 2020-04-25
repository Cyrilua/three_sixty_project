from django.contrib import auth
from django.shortcuts import redirect
from django.shortcuts import render

from main.models import Profile


def get_user_profile(request):
    user = auth.get_user(request)
    return Profile.objects.get(user=user)


def get_photo_height(width, height):
    result = round(177 / (width / height))
    if result > 300:
        result = 300
    return result


def find_user(request, action_with_selected_user='main:profile'):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {
        'title': "Поиск пользователей",
        'redirect': action_with_selected_user,
    }
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
        print(1)
        for i in profiles:
            print(i)
        return render(request, 'main/search_profile.html', args)

    return render(request, 'main/search_profile.html', args)


def valid_input(user_input: str):
    return user_input is not None and user_input != ''


def filter_profile(func, profiles):
    if profiles is None:
        return filter(func, Profile.objects.all())
    return filter(func, profiles)
