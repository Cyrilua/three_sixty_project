import datetime

from main.forms import ProfileForm, PhotoProfileForm, UserChangeEmailForm
from main.models import ProfilePhoto, BirthDate, PositionCompany, PlatformCompany
from main.views.auxiliary_general_methods import *

from django.http import JsonResponse


def profile_view(request, profile_id=-1):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if profile_id == get_user_profile(request).id or profile_id == -1:
        return get_render_user_profile(request)
    return get_other_profile_render(request, profile_id)


def get_render_user_profile(request):
    profile = get_user_profile(request)
    try:
        photo = profile.profilephoto.photo
    except:
        photo = None

    profile_data = {
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic,
            'roles': []
        }

    company = profile.company
    print(company)
    print(company.owner.id)
    print(auth.get_user(request).id)
    if company is not None and company.owner.id == auth.get_user(request).id:
        profile_data['roles'].append('boss')
    try:
        SurveyWizard.objects.get(profile=profile)
    except:
        pass
    else:
        profile_data['roles'].append('master')
    try:
        Moderator.objects.get(profile=profile)
    except:
        pass
    else:
        profile_data['roles'].append('moderator')
    print(profile_data['roles'])
    profile_data['company'] = {
        'url': '/company_view/',
        'name': company.name,
    }

    if profile.platform is not None:
        profile_data['platform'] = profile.platform
    if profile.position is not None:
        profile_data['position'] = profile.position
    try:
        profile_data['birthdate'] = BirthDate.objects.get(profile=profile)
    except:
        pass
    try:
        profile_data['email'] = auth.get_user(request).email
    except:
        pass
    teams = []
    for team in profile.groups.all():
        teams.append({
            'url': 'command/{}/'.format(team.id),
            'name': team.name
        })
    if len(teams) != 0:
        profile_data['teams'] = teams
    args = {
        "title": "Главная",
        'photo': photo,
        'profile': profile_data,
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
    return render(request, "main/user/old/upload_photo.html", args)


def edit_profile(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    user = auth.get_user(request)
    profile = get_user_profile(request)
    try:
        birth_date = BirthDate.objects.get(profile=profile)
    except:
        birth_date = datetime.datetime.strptime('1900-1-1', '%Y-%m-%d')
    args = {
        'title': "Редактирование профия",
        'profile_form': ProfileForm({
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic,
            'birthday': birth_date}),
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
    return render(request, 'main/user/old/edit_profile.html', args)



