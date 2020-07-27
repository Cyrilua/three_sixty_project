import datetime

from main.forms import PhotoProfileForm
from main.models import ProfilePhoto, PlatformCompany, PositionCompany, BirthDate
from main.views.auxiliary_general_methods import *
from .render_profile import build_profile_data
from main.views import validators
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm


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
    try:
        birth_date = args['profile']['birthdate']
        args['profile']['birthdate'] = {
            'text': birth_date,
            'date': '{}.{}.{}'.format(birth_date.day, birth_date.month, birth_date.year)
        }
    except KeyError:
        pass
    company = profile.company
    if company is not None:
        positions = company.positioncompany_set.all()
        profile_positions = profile.positions.all()
        args['new_positions'] = _build_objects(filter(lambda x: x not in profile_positions, positions))

        platform = company.platformcompany_set.all()
        profile_platforms = profile.platforms.all()
        args['new_platforms'] = _build_objects(filter(lambda x: x not in profile_platforms, platform))

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
    if request.is_ajax():
        platform = PlatformCompany.objects.get(id=platform_id)
        platform.profile_set.remove(get_user_profile(request))
        return JsonResponse({'resultStatus': 'success'}, status=200)


def remove_position(request, position_id: int) -> redirect:
    if request.is_ajax():
        position = PositionCompany.objects.get(id=position_id)
        position.profile_set.remove(get_user_profile(request))
        return JsonResponse({'resultStatus': 'success'}, status=200)


def add_platform(request, platform_id: int) -> redirect:
    if request.is_ajax():
        profile = get_user_profile(request)
        platform = PlatformCompany.objects.get(id=platform_id)
        platform.profile_set.add(profile)
        return JsonResponse({'resultStatus': 'success'}, status=200)


def add_position(request, position_id: int) -> redirect:
    if request.is_ajax():
        profile = get_user_profile(request)
        position = PositionCompany.objects.get(id=position_id)
        position.profile_set.add(profile)
        return JsonResponse({'resultStatus': 'success'}, status=200)


def _get_result(errors: list) -> JsonResponse:
    if len(errors) == 0:
        return JsonResponse({'resultStatus': 'success'}, status=200)
    return JsonResponse({'resultStatus': 'error',
                         'resultError': errors}, status=200)


def _get_value(data) -> str:
    key = 'values[{}]'.format(data['id'])
    return data[key]


def check_name(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        errors = validators.validate_name(value)
        # TODO сравнивать с текущим значением в бд
        return _get_result(errors)


def check_surname(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        errors = validators.validate_surname(value)
        return _get_result(errors)


def check_patronymic(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        errors = validators.validate_patronymic(value)
        return _get_result(errors)


def save_changes_fcs(request) -> JsonResponse:
    if request.is_ajax():
        data = request.POST
        profile = get_user_profile(request)
        profile.name = data['values[name]']
        profile.surname = data['values[surname]']
        profile.patronymic = data['values[patronymic]']
        profile.save()
        return JsonResponse({'resultStatus': 'success'}, status=200)


def check_birth_date(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        errors = validators.validate_birth_date(value)
        return _get_result(errors)


def save_birth_date(request) -> JsonResponse:
    if request.is_ajax():
        date = request.POST['values[birthdate]']
        try:
            birth_date = datetime.datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            return JsonResponse({'resultStatus': 'error'}, status=400)
        profile = get_user_profile(request)
        try:
            birth_date_profile = BirthDate.objects.get(profile=profile)
            birth_date_profile.birthday = birth_date
        except ObjectDoesNotExist:
            birth_date_profile = BirthDate()
            birth_date_profile.profile = profile
            birth_date_profile.birthday = birth_date
        birth_date_profile.save()
        return JsonResponse({'resultStatus': 'success'}, status=200)


def check_login(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        if value == auth.get_user(request).username:
            return JsonResponse({'resultStatus': 'error',
                                 'resultError': []}, status=200)
        errors = validators.validate_login(value)
        return _get_result(errors)


def save_login(request) -> JsonResponse:
    if request.is_ajax():
        user = auth.get_user(request)
        new_username = request.POST['values[username]']
        user.username = new_username
        user.save()
        return JsonResponse({'resultStatus': 'success'}, status=200)


from django.contrib.auth.hashers import check_password


def check_old_password(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        user = auth.get_user(request)
        result = user.check_password(value)
        return JsonResponse({'resultStatus': 'success'}, status=200)
