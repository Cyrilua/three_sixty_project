import datetime

from main.forms import PhotoProfileForm
from main.models import ProfilePhoto, PlatformCompany, PositionCompany, BirthDate
from main.views.auxiliary_general_methods import *
from .render_profile import build_profile_data
from main.views import validators
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.http import JsonResponse


from PIL import Image

from django.conf import settings
from django.core.files.storage import FileSystemStorage


@csrf_exempt
def upload_profile_photo(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        #print(request.FILES)
        user_photo = request.FILES['0']
        profile = get_user_profile(request)
        try:
            photo_profile = ProfilePhoto.objects.get(profile=profile)
        except ObjectDoesNotExist:
            pass
        else:
            photo_profile.delete()
        photo_profile = ProfilePhoto()
        photo_profile.profile = profile
        photo_profile.photo = user_photo
        photo_profile.save()

        result = photo_profile.photo.url
        print(result)
        return JsonResponse({'new_photo_url': photo_profile.photo.url}, status=200)


def delete_profile_photo(request) -> render:
    if request.is_ajax():
        try:
            photo = ProfilePhoto.objects.get(profile=get_user_profile(request))
        except ObjectDoesNotExist:
            return JsonResponse({}, status=200)
        else:
            photo.delete()
        return JsonResponse({}, status=200)


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

    #img = Image.open(photo)
    #img_str = img.tobytes()
    #test = profile.profilephoto
    #test.photo_hex = img_str
    #test.save()

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
        profile = get_user_profile(request)
        if value == profile.name:
            return JsonResponse({'resultStatus': 'error',
                                 'resultError': []}, status=200)
        return _get_result(errors)


def check_surname(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        errors = validators.validate_surname(value)
        profile = get_user_profile(request)
        if value == profile.surname:
            return JsonResponse({'resultStatus': 'error',
                                 'resultError': []}, status=200)
        return _get_result(errors)


def check_patronymic(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        errors = validators.validate_patronymic(value)
        profile = get_user_profile(request)
        if value == profile.patronymic:
            return JsonResponse({'resultStatus': 'error',
                                 'resultError': []}, status=200)
        return _get_result(errors)


def save_changes_fcs(request) -> JsonResponse:
    if request.is_ajax():
        data = request.POST
        profile = get_user_profile(request)
        profile.name = data['values[name]']
        profile.surname = data['values[surname]']
        profile.patronymic = data['values[patronymic]']
        profile.save()
        args = {
            'resultStatus': 'success',
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic
        }
        return JsonResponse(args, status=200)


def check_birth_date(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        errors = validators.validate_birth_date(value)
        if len(errors) == 0:
            date = datetime.datetime.strptime(value, '%d.%m.%Y')
            try:
                profile_date = BirthDate.objects.get(profile=get_user_profile(request)).birthday
            except ObjectDoesNotExist:
                pass
            else:
                if date.day == profile_date.day and date.month == profile_date.month and profile_date.year == date.year:
                    return JsonResponse({'resultStatus': 'error',
                                         'resultError': []}, status=200)
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
        args = {
            'resultStatus': 'success',
            'birthdate': {
                'text': birth_date_profile.birthday,
                'date': '{}.{}.{}'.format(birth_date.day, birth_date.month, birth_date.year)
            }
        }
        return JsonResponse(args, status=200)


def check_email(request) -> JsonResponse:
    if request.is_ajax():
        value = _get_value(request.POST)
        user = auth.get_user(request)
        if user.email == value:
            return JsonResponse({'resultStatus': 'error',
                                 'resultError': []}, status=200)
        errors = validators.validate_email(value)
        return _get_result(errors)


def save_email(request) -> JsonResponse:
    if request.is_ajax():
        value = request.POST['values[email]']
        user = auth.get_user(request)
        password = request.POST['values[password_for_email]']
        args = {
            'email': value,
            'resultStatus': 'success'
        }
        if not user.check_password(password):
            args['resultStatus'] = 'error'
            args['listErrors'] = {'password_for_email': ['Неверный пароль']}
            return JsonResponse(args, status=200)
        user.email = value
        user.save()
        profile = get_user_profile(request)
        profile.email_is_validate = False
        profile.save()
        code = create_verification_code(user.email)
        send_email_validate_message(profile.name, profile.surname, user.email, code)

        return JsonResponse(args, status=200)


def check_email_code(request):
    if request.is_ajax():
        user = request.user
        errors = validators.validate_code(request.POST['values[email_code]'], get_user_profile(request))
        args = {
            'email': user.email,
            'resultStatus': 'success'
        }
        if len(errors) != 0:
            args['resultStatus'] = 'error'
            args['listErrors'] = errors
            return JsonResponse(args, status=200)
        profile = get_user_profile(request)
        profile.email_is_validate = True
        return JsonResponse(args, status=200)


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
        args = {
            'resultStatus': 'success',
            'username': new_username
        }
        return JsonResponse(args, status=200)


def check_new_password_1(request) -> JsonResponse:
    if request.is_ajax():
        password_1 = _get_value(request.POST)
        errors = validators.validate_password1(password_1)
        return _get_result(errors)


def check_new_password_2(request) -> JsonResponse:
    if request.is_ajax():
        password1 = request.POST['values[password1]']
        password2 = request.POST['values[password2]']
        errors = validators.validate_password2(password2, password1)
        return _get_result(errors)


def save_new_password(request) -> JsonResponse:
    if request.is_ajax():
        data = {
            'old_password': request.POST['values[password_old]'],
            'new_password1': request.POST['values[password1]'],
            'new_password2': request.POST['values[password2]']
        }
        password_change = PasswordChangeForm(request.user, data)
        if password_change.is_valid():
            password_change.save()
            update_session_auth_hash(request, password_change.user)
        else:
            return JsonResponse({'resultStatus': 'error',
                                 'listErrors': password_change.errors}, status=200)
        return JsonResponse({'resultStatus': 'success'}, status=200)
