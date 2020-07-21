import datetime

from main.forms import ProfileForm, PhotoProfileForm, UserChangeEmailForm
from main.models import ProfilePhoto, BirthDate, Notifications, Poll, Company, Group
from main.views.auxiliary_general_methods import *

from django.core.exceptions import ObjectDoesNotExist


def profile_view(request, profile_id):
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

    profile_data = build_profile_data(auth.get_user(request), get_user_profile(request))

    args = {
        "title": "Главная",
        'photo': photo,
        'profile': profile_data[0],
        'roles': profile_data[1],
        'notifications': build_notifications(profile)
    }
    return render(request, 'main/user/profile.html', args)


def build_profile_data(user, profile):
    profile_data = {
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic,
            'teams': get_user_teams(profile)
        }

    company = profile.company
    roles = []
    if company is not None:
        roles = get_user_roles(user, profile, company)
        profile_data['company'] = {
            'url': '/company_view/{}/'.format(company.id),
            'name': company.name,
        }

        if profile.platform is not None:
            profile_data['platform'] = profile.platform
        if profile.position is not None:
            profile_data['position'] = profile.position

    try:
        profile_data['birthdate'] = BirthDate.objects.get(profile=profile).birthday
    except ObjectDoesNotExist:
        pass

    try:
        profile_data['email'] = user.email
    except ObjectDoesNotExist:
        pass
    return [profile_data, roles]


def get_user_roles(user, profile, company):
    roles = []
    if company is not None and company.owner.id == user.id:
        roles.append('boss')
    try:
        SurveyWizard.objects.get(profile=profile)
    except ObjectDoesNotExist:
        pass
    else:
        roles.append('master')

    try:
        Moderator.objects.get(profile=profile)
    except ObjectDoesNotExist:
        pass
    else:
        roles.append('moderator')
    return roles


def get_user_teams(profile):
    teams = []
    for team in profile.groups.all():
        teams.append({
            'url': '/team/{}/'.format(team.id),
            'name': team.name
        })
    return teams


def build_notifications(profile):
    notifications = Notifications.objects.filter(profile=profile)
    my_polls = []
    polls = []
    invites = []
    for notif in notifications:
        if notif.type == 'my_poll':
            try:
                poll = Poll.objects.get(id=notif.key)
            except:
                continue
            collected_notification = {
                'url': notif.url.format(notif.key),
                'date': notif.date,
                'title': notif.name,
                'more': {
                    'name': "{} {} {}".format(notif.on_profile.surname, notif.on_profile.name,
                                              notif.on_profile.patronymic),
                    'url': '/{}/'.format(notif.on_profile.id)
                },
                'about': '{} ответов'.format(poll.count_passed),
                'complited': notif.completed
            }
            my_polls.append(collected_notification)

        elif notif.type == 'invite_company':
            try:
                company = Company.objects.get(key=notif.key)
            except:
                continue
            collected_notification = {
                'url': notif.url.format(notif.key),
                'date': notif.date,
                'title': {
                    'name': notif.name,
                    'url': '/company_view/{}/'.format(company.id),
                },
                'more': {
                    'name': "{} {} {}".format(notif.from_profile.surname, notif.from_profile.name,
                                              notif.from_profile.patronymic),
                    'url': '/{}/'.format(notif.from_profile.id)
                },
                'about': company.description,
                'complited': notif.completed
            }
            invites.append(collected_notification)
        elif notif.type == 'invite_command':
            try:
                command = Group.objects.get(key=notif.key)
            except:
                continue
            collected_notification = {
                'url': notif.url.format(notif.key),
                'date': notif.date,
                'title': {
                    'name': notif.name,
                    'url': '/company_view/{}/'.format(command.id),
                },
                'more': {
                    'name': "{} {} {}".format(notif.from_profile.surname, notif.from_profile.name,
                                              notif.from_profile.patronymic),
                    'url': '/{}/'.format(notif.from_profile.id)
                },
                'about': command.description,
                'complited': notif.completed
            }
            invites.append(collected_notification)
        elif notif.type == 'alien_poll':
            try:
                poll = Poll.objects.get(id=notif.key)
            except:
                continue
            collected_notification = {
                'url': notif.url.format(notif.key),
                'date': notif.date,
                'title': notif.name,
                'more': {
                    'name': "{} {} {}".format(notif.from_profile.surname, notif.from_profile.name,
                                              notif.from_profile.patronymic),
                    'url': '/{}/'.format(notif.from_profile.id)
                },
                'about': poll.description,
                'complited': notif.completed
            }
            polls.append(collected_notification)
        return {
            'polls': polls,
            'my_polls': my_polls,
            'invites': invites
        }


def get_other_profile_render(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    try:
        photo = profile.profilephoto.photo
    except:
        photo = None

    profile_data = build_profile_data(profile.user, profile)

    args = {
        "title": "Просмотр профиля пользователя",
        'photo': photo,
        'alien_profile': profile_data[0],
        'roles': profile_data[1],
    }
    print(args)
    return render(request, "main/user/alien_profile.html", args)


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

