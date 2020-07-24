from main.forms import PhotoProfileForm
from main.models import ProfilePhoto, PlatformCompany, PositionCompany
from main.views.auxiliary_general_methods import *
from .render_profile import build_profile_data

from django.http import JsonResponse


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
    return render(request, "main/user/old/upload_photo.html", args)


def edit_profile(request) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    user = auth.get_user(request)
    profile = get_user_profile(request)
    try:
        photo = profile.profilephoto.photo
    except:
        photo = None
    profile_data = build_profile_data(user, profile)

    args = {
        'title': "Настройки",
        'photo': photo,
        'profile': profile_data[0],
        'roles': profile_data[1],
    }

    args['profile']['login'] = user.username
    birth_date = args['profile']['birthdate']
    args['profile']['birthdate'] = {
        'text': birth_date,
        'date': '{}.{}.{}'.format(birth_date.day, birth_date.month, birth_date.year)
    }
    company = profile.company
    if company is not None:
        positions = company.positioncompany_set.all()
        profile_positions = profile.positions.all()
        args['new_positions'] = _build_objects(filter(lambda x: x not in profile_positions, positions))

        platform = company.platformcompany_set.all()
        profile_platform = profile.platforms.all()
        args['new_platforms'] = _build_objects(filter(lambda x: x not in profile_platform, platform))

    if request.method == 'POST':
        print(request.POST)
    return render(request, 'main/user/edit.html', args)


def _build_objects(list_objects: filter) -> list:
    result = []
    for pos in list_objects:
        completed = {
            'id': pos.id,
            'name': pos.name
        }
        result.append(completed)
    return result


def remove_platform(request, platform_id: int) -> redirect:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    print('i am here')
    if request.is_ajax():
        print('i am here !')
        platform = PlatformCompany.objects.get(id=platform_id)
        platform.profile_set.remove(get_user_profile(request))
        return JsonResponse({'resultStatus': 'success'}, status=200)
