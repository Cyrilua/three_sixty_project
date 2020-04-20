from django.shortcuts import redirect
from django.shortcuts import render

from main.forms import ProfileForm, PhotoProfileForm
from main.models import ProfilePhoto
from main.views.auxiliary_general_methods import *


def get_user_profile(request):
    user = auth.get_user(request)
    return Profile.objects.get(user=user)


def get_photo_height(width, height):
    result = round(177 / (width / height))
    if result > 300:
        result = 300
    return result


def profile_view(request, profile_id=-1):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if profile_id == get_user_profile(request).id or profile_id == -1:
        return get_render_user_profile(request)
    return get_other_profile_render(request, profile_id)


def get_render_user_profile(request):
    profile = get_user_profile(request)

    rating = 0
    if profile.count_answers > 0:
        rating = profile.answers_sum / profile.count_answers

    last_poll = profile.last_poll

    try:
        photo = profile.profilephoto.photo
    except:
        photo = None

    args = {
        "title": "Мой профиль",
        'profile': profile,
        'rating': rating,
        'last_poll': last_poll,
        'photo': photo,
    }
    if photo is not None:
        args['photo_height'] = get_photo_height(photo.width, photo.height)

    return render(request, 'main/profile.html', args)


def get_other_profile_render(request, profile_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = Profile.objects.get(id=profile_id)
    args = {
        'title': "Профиль просматриваемого пользователя",
        'name': profile.name,
        'surname': profile.surname,
        'patronymic': profile.patronymic,
        'groups': profile.groups.all(),
    }

    try:
        args['photo'] = profile.profilephoto.photo
    except:
        args['photo'] = None

    if args['photo'] is not None:
        args['photo_height'] = get_photo_height(args['photo'].width, args['photo'].height)

    try:
        args['position'] = profile.position.name
    except:
        args['position'] = None

    try:
        args['company'] = profile.company.name
    except:
        args['company'] = None

    try:
        args['platform'] = profile.platform.name
    except:
        args['platform'] = None

    return render(request, "main/alien_profile.html", args)


def upload_profile_photo(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    args = {
        'title': "Добавление фотографии пользователя",
        'form': PhotoProfileForm()
    }

    if request.method == "POST":
        user_photo = request.FILES['photo']
        try:
            profile.profilephoto.photo = user_photo
            profile.profilephoto.save()
        except:
            photo_profile = ProfilePhoto()
            photo_profile.photo = user_photo
            photo_profile.profile = profile
            photo_profile.save()
        return redirect('/')
    return render(request, "main/upload_photo.html", args)





def edit_profile(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {}
    profile = get_user_profile(request)
    try:
        photo = profile.profilephoto.photo
        args['photo'] = photo
        args['photo_height'] = get_photo_height(photo.width, photo.height)
    except:
        args['photo'] = None

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile.name = request.POST.get('name', '')
            profile.patronymic = request.POST.get('patronymic', '')
            profile.surname = request.POST.get('surname', '')
            profile.city = request.POST.get('city', '')
            profile.save()
    args['profile_form'] = ProfileForm({
        'name': profile.name,
        'surname': profile.surname,
        'patronymic': profile.patronymic,
        'city': profile.city,
    })
    args['title'] = "Редактирование профия"
    args['profile'] = profile
    return render(request, 'main/edit_profile.html', args)



