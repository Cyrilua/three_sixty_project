from main.forms import ProfileForm, PhotoProfileForm, UserChangeEmailForm
from main.models import ProfilePhoto
from main.views.auxiliary_general_methods import *

from django.http import JsonResponse


def profile_view(request, profile_id=-1):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if profile_id == get_user_profile(request).id or profile_id == -1:
        return get_render_user_profile(request)
    return get_other_profile_render(request, profile_id)


def get_render_user_profile(request):
    # if request.is_ajax():
    #     if request.method == "GET":
    #         text = request.GET.get('button_text')
    #         return JsonResponse({'result_1': text}, status=200)
    #     if request.method == "POST":
    #         span_text = request.POST.get('text')
    #         return JsonResponse({'data_result': span_text}, status=200)

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
    args['teams'] = profile.groups.all()

    return render(request, 'main/user/profile.html', args)


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

    profile_photo = ProfilePhoto.objects.filter(profile=profile)
    if len(profile_photo) != 0:
        args['photo'] = profile_photo[0].photo
        args['photo_height'] = get_photo_height(args['photo'].width, args['photo'].height)
    else:
        args['photo'] = None

    if profile.position is not None:
        args['position'] = profile.position.name
    else:
        args['position'] = 'не указано'

    if profile.company is not None:
        args['company'] = profile.company.name
    else:
        args['company'] = 'не указано'

    if profile.platform is not None:
        args['platform'] = profile.platform.platform.name
    else:
        args['platform'] = 'не указано'

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
    return render(request, "main/user/upload_photo.html", args)


def edit_profile(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    user = auth.get_user(request)
    profile = get_user_profile(request)
    args = {
        'title': "Редактирование профия",
        'profile_form': ProfileForm({
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic,
            'city': profile.city}),
        'email_form': UserChangeEmailForm({'email': user.email}),
        'profile': profile,
        'user': user
    }

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
        email_form = UserChangeEmailForm(request.POST)
        if email_form.is_valid():
            new_email = request.POST.get('email', '')
            user.email = new_email
            user.save()
        return redirect('/edit/')
    return render(request, 'main/user/edit_profile.html', args)



