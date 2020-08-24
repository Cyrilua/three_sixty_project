import uuid

from django.shortcuts import redirect, render
from main.forms import CompanyForm
from main.models import Company, PlatformCompany, PositionCompany, PositionCompany, PlatformCompany, ProfilePhoto, \
    SurveyWizard, Moderator, Group
from main.views.auxiliary_general_methods import *
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.template.response import SimpleTemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from .validators import validate_user_input_in_company_settings


def add_new_platform(request):
    # Не используется
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {'title': 'Добавление новой платформы'}
    if request.method == "POST":
        new_platform = request.POST.get("platform", '').lower()
        try:
            PlatformCompany.objects.get(name=new_platform)
        except:
            platform = PlatformCompany(name=new_platform)
            platform.save()
            return redirect('/')
        else:
            args['error'] = "Эта платформа уже существует"
            return render(request, 'main/add_new_platform.html', args)
    return render(request, 'main/add_new_platform.html', args)


def add_new_position(request):
    # Не используется
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {'title': 'Добавление новой должности'}
    if request.method == "POST":
        new_position = request.POST.get("position", '').lower()
        try:
            PositionCompany.objects.get(name=new_position)
        except:
            position = PositionCompany(name=new_position)
            position.save()
            return redirect('/')
        else:
            args['error'] = "Эта должность уже существует"
            return render(request, 'main/add_new_position.html', args)
    return render(request, 'main/add_new_position.html', args)


def create_company(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    user = auth.get_user(request)
    profile = get_user_profile(request)

    args = {'title': "Создание компании",
            'company_form': CompanyForm()}

    if profile.company is not None:
        return redirect('/communications/')

    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.owner = user
            company.key = uuid.uuid4().__str__()
            company.save()

            profile.company = company
            profile.save()

            return redirect('/communications/')
        else:
            args['company_form'] = company_form
    return render(request, 'main/companies/old/add_new_company.html', args)


def connect_to_company_to_key(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    args = {'company_form': CompanyForm(),
            'title': "Добавление участников"}

    if profile.company is not None:
        return redirect('/communications/')

    if request.method == 'POST':
        try:
            key_company = request.POST.get("key", '')
            company = Company.objects.get(key=key_company)
        except:
            return redirect('/communications/')
        else:
            add_user_to_company(profile, company)
            return redirect('/communications/')

    return render(request, 'main/companies/old/connect_to_company.html', args)


def add_user_to_company(profile, company):
    right_position = list(filter(lambda x: x.position == profile.position, company.positioncompany_set.all()))
    right_platform = list(filter(lambda x: x.platform == profile.platform, company.platformcompany_set.all()))

    if len(right_position) != 0:
        profile.position = None

    if len(right_platform) != 0:
        profile.platform = None

    profile.company = company
    profile.save()


def connect_to_company_to_link(request, key):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    if profile.company is not None:
        return redirect('/communications/')

    try:
        company = Company.objects.get(key=key)
    except:
        return redirect('/communications/')
    else:
        add_user_to_company(profile, company)
        return redirect('/communications/')


def get_all_users_in_company(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    company = profile.company
    args = {"title": "Все пользователи компании"}
    try:
        users = company.profile_set.all()
    except:
        args['error'] = "Пользователь не состоит в компании"
        return render(request, 'main/users_company.html', args)
    else:
        args['user'] = users
        return render(request, 'main/users_company.html', args)


def add_position_in_company(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    company = profile.company
    args = {'title': "Добавление должности в компанию"}
    if company is None:
        args['error'] = "Пользователь не состоит в компании"
        return render(request, 'main/add_new_position.html', args)

    if company.owner != auth.get_user(request) and not user_is_admin_in_current_company(request):
        args['error'] = 'У пользователя нет достаточного доступа для этой операции'
        return render(request, 'main/add_new_position.html', args)

    if request.method == "POST":
        position_name = request.POST.get('position', '')
        try:
            position = PositionCompany.objects.get(name=position_name)
        except:
            position = PositionCompany(name=position_name)
            position.save()

        positions_in_company = PositionCompany.objects.filter(company=company)
        for i in positions_in_company:
            if i.position.id == position.id:
                args['error'] = "Эта должность уже выбрана для этой компании"
                return render(request, 'main/add_new_position.html', args)

        position_in_company = PositionCompany()
        position_in_company.position = position
        position_in_company.company = company
        position_in_company.save()

        return redirect('/')
    return render(request, 'main/add_new_position.html', args)


def add_platform_in_company(request):
    # Не используется
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {'title': "Добавление платформы в компанию"}
    profile = get_user_profile(request)
    company = profile.company

    if company is None:
        args['error'] = "Пользователь не состоит в компании"
        return render(request, 'main/add_new_platform.html', args)

    if company.owner != auth.get_user(request) and not user_is_admin_in_current_company(request):
        args['error'] = 'У пользователя нет достаточного доступа для этой операции'
        return render(request, 'main/add_new_position.html', args)

    if request.method == "POST":
        platform_name = request.POST.get('platform', '')
        try:
            platform = PlatformCompany.objects.get(name=platform_name)
        except:
            platform = PlatformCompany(name=platform_name)
            platform.save()

        platforms_in_company = PlatformCompany.objects.filter(company=company)
        for i in platforms_in_company:
            if i.platform.id == platform.id:
                args['error'] = "Эта платформа уже выбрана для этой компании"
                return render(request, 'main/add_new_platform.html', args)

        platform_in_company = PlatformCompany()
        platform_in_company.platform = platform
        platform_in_company.company = company
        platform_in_company.save()

        return redirect('/company_view/')
    return render(request, 'main/add_new_platform.html', args)


def choose_position(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    company = profile.company
    args = {
        'title': "Список всех должностей в компании",
        'profile': profile,
        'company': company
    }
    if company is None:
        args['list_positions'] = PositionCompany.objects.all()
    else:
        args['list_positions'] = [i.position for i in company.positioncompany_set.all()]

    if request.method == "POST":
        position_id = request.POST.get('id_position', '')
        if int(position_id) == -1:
            profile.position = None
            profile.save()
            return redirect('/communications/')
        try:
            position = PositionCompany.objects.get(id=position_id)
        except:
            args['error'] = 'Данной должности не существует'
            return render(request, 'main/position_choice.html', args)

        if position not in args['list_positions']:
            args['error'] = "Выбранная должность отсутствует в списке"
            return render(request, 'main/position_choice.html', args)

        profile.position = position
        profile.save()
        return redirect('/communications/')

    return render(request, 'main/position_choice.html', args)


def choose_platform(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    company = profile.company
    args = {
        'title': "Список всех должностей в компании",
        'profile': profile,
        'company': company
    }
    if company is None:
        args['list_platforms'] = PlatformCompany.objects.all()
    else:
        args['list_platforms'] = [i.platform for i in company.platformcompany_set.all()]
    if request.method == "POST":
        platform_id = request.POST.get('id_platform', '')
        if platform_id == -1:
            return redirect('/communications/')
        try:
            platform = PlatformCompany.objects.get(id=platform_id)
        except:
            args['error'] = 'Данной платформы не существует'
            return render(request, 'main/platform_choice.html', args)

        platform_company = PlatformCompany.objects.get(platform=platform)
        if platform_company is None:
            args['error'] = "Выбранная платформа отсутствует в списке"
            return render(request, 'main/platform_choice.html', args)

        profile.platform = platform_company
        profile.save()
        return redirect('/communications/')
    return render(request, 'main/platform_choice.html', args)


######## new company view ##########

def company_view(request: WSGIRequest, id_company: int):
    # todo
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.method == "GET":
        company: Company = Company.objects.filter(pk=id_company).first()
        if company is None:
            # todo throw exception
            pass
        profile = get_user_profile(request)
        args = {
            #'users': _build_profiles(company),
            'profile': {
                'is_boss': company.owner == profile,
                'is_master': SurveyWizard.objects.filter(profile=profile).exists()
            },
            'company': {
                'name': company.name,
                'description': company.description,
                'positions': PositionCompany.objects.filter(company=company),
                'platforms': PlatformCompany.objects.filter(company=company),
                'countParticipants': company.profile_set.all().count(),
                'countTeams': Group.objects.filter(company=company).count()
            }
        }
        return render(request, 'main/companies/company_view.html', args)


def load_teams_and_users(request: WSGIRequest, id_company: int) -> JsonResponse:
    if request.is_ajax():
        try:
            category = request.GET['category']
        except MultiValueDictKeyError:
            return JsonResponse({}, status=404)
        company: Company = Company.objects.filter(pk=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)
        if category == 'users':
            content = _load_users(company, get_user_profile(request))
        elif category == 'teams':
            content = _load_teams(company, get_user_profile(request))
        return JsonResponse({'content': content}, status=200)


def _load_users(company: Company, profile: Profile):
    collected_profiles = _build_profiles(company)
    args = {
        'users': collected_profiles,
        'profile': {
            'is_boss': company.owner == profile,
            'is_moderator': Moderator.objects.filter(profile=profile).exists()
        }
    }
    return SimpleTemplateResponse('main/companies/users.html', args).rendered_content


def _build_profiles(company: Company):
    result = []
    profiles = company.profile_set.all()
    for profile in profiles:
        profile: Profile
        try:
            photo = ProfilePhoto.objects.get(profile=profile).photo
        except ObjectDoesNotExist:
            photo = None
        collected_profile = {
            'id': profile.pk,
            'photo': photo,
            'href': '/{}/'.format(profile.pk),
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic,
            'roles': _get_roles(profile),
            'new_roles': _get_new_roles(profile),
            'positions': profile.positions.all(),
            'new_positions': PositionCompany.objects.filter(company=company).exclude(profile=profile),
            'platforms': profile.platforms.all(),
            'new_platforms': PlatformCompany.objects.filter(company=company).exclude(profile=profile),
        }
        result.append(collected_profile)
    return result


def _load_teams(company: Company, profile: Profile):
    teams = Group.objects.filter(company=company)
    collected_teams = []
    for team in teams:
        team: Group
        collected_teams.append({
            'id': team.pk,
            'href': '',  # todo
            'name': team.name,
            'quantity': team.profile_set.all().count(),
            'description': team.description,
        })
    args = {
        'teams': collected_teams,
        'profile': {
            'is_boss': company.owner == profile,
            'is_moderator': Moderator.objects.filter(profile=profile).exists()
        }
    }
    return SimpleTemplateResponse('main/companies/teams.html', args).rendered_content


def remove_team(request: WSGIRequest, team_id: int):
    if request.is_ajax():
        profile = get_user_profile(request)
        team = Group.objects.filter(id=team_id).first()
        if team is None:
            return JsonResponse({}, status=404)
        if not _profile_is_owner_or_moderator(profile):
            return JsonResponse({}, status=403)
        team.delete()
        return JsonResponse({}, status=200)


def _profile_is_owner_or_moderator(profile: Profile):
    company = profile.company
    is_owner = False
    if company is not None:
        is_owner = company.owner == profile
    return Moderator.objects.filter(profile=profile).exists() or is_owner


def company_setting(request: WSGIRequest, id_company: int):
    # todo
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.method == "GET":
        profile = get_user_profile(request)
        company = Company.objects.filter(pk=id_company).first()
        if company is None:
            return render(request, 'main/errors/global_error.html', {'global_error': 404})
        args = {
            'company': {
                'name': company.name,
                'description': company.description,
                'hrefForInvite': '',  # todo
                'positions': PositionCompany.objects.filter(company=company),
                'platforms': PlatformCompany.objects.filter(company=company),
                'countParticipants': company.profile_set.all().count(),
                'countTeams': Group.objects.filter(company=company).count()
            },
            'profile': {
                'is_boss': company.owner == profile,
                'is_moderator': Moderator.objects.filter(profile=profile).exists()
            }
        }
        return render(request, 'main/companies/company_setting.html', args)


def _get_roles(profile: Profile) -> list:
    roles = []
    if profile.company.owner.pk == profile.pk:
        roles.append('boss')
    if SurveyWizard.objects.filter(profile=profile).exists():
        roles.append('master')
    if Moderator.objects.filter(profile=profile).exists():
        roles.append('moderator')
    return roles


def _get_new_roles(profile: Profile) -> list:
    roles = []
    if not SurveyWizard.objects.filter(profile=profile).exists():
        roles.append('master')
    if not Moderator.objects.filter(profile=profile).exists():
        roles.append('moderator')
    return roles


def add_position(request: WSGIRequest, id_company) -> JsonResponse:
    if request.is_ajax():
        company = Company.objects.filter(pk=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)
        profile = get_user_profile(request)
        if not _profile_is_owner_or_moderator(profile):
            return JsonResponse({}, status=403)
        name_position = request.POST['namePosition']
        if not validate_user_input_in_company_settings(name_position):
            return JsonResponse({}, status=400)

        position = PositionCompany()
        position.name = name_position
        position.company = company
        position.save()
        return JsonResponse({}, status=200)


def remove_position(request: WSGIRequest, id_company: int, position_id: int) -> JsonResponse:
    if request.is_ajax():
        company = Company.objects.filter(pk=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)
        profile = get_user_profile(request)
        if not _profile_is_owner_or_moderator(profile):
            return JsonResponse({}, status=403)
        position = PositionCompany.objects.filter(id=position_id).first()
        if position is None:
            return JsonResponse({}, status=404)

        position.delete()
        return JsonResponse({}, status=200)


def add_platform(request: WSGIRequest, id_company):
    if request.is_ajax():
        company = Company.objects.filter(pk=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)
        profile = get_user_profile(request)
        if not _profile_is_owner_or_moderator(profile):
            return JsonResponse({}, status=403)
        name_platform = request.POST['namePlatform']
        if not validate_user_input_in_company_settings(name_platform):
            return JsonResponse({}, status=400)

        platform = PlatformCompany()
        platform.name = name_platform
        platform.company = company
        platform.save()
        return JsonResponse({}, status=200)
