import uuid

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.response import SimpleTemplateResponse

from main.forms import CompanyForm
from main.models import Company, PositionCompany, PlatformCompany, ProfilePhoto, \
    SurveyWizard, Moderator, Group
from main.views.auxiliary_general_methods import *
from .validators import validate_user_input_in_company_settings


def create_company(request):
    # todo temp
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    user = auth.get_user(request)
    profile = get_user_profile(request)

    args = {'title': "Создание компании",
            'company_form': CompanyForm()}

    if profile.company is not None:
        return redirect('/')

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
            'company': {
                'id': company.pk,
                'name': company.name,
                'description': company.description,
                'positions': PositionCompany.objects.filter(company=company),
                'platforms': PlatformCompany.objects.filter(company=company),
                'countParticipants': company.profile_set.all().count(),
                'countTeams': Group.objects.filter(company=company).count()
            },
            'profile': get_header_profile(profile)
        }
        args['profile']['is_boss'] = company.owner == profile
        args['profile']['is_master'] = SurveyWizard.objects.filter(profile=profile).exists()
        return render(request, 'main/companies/company_view.html', args)


def load_teams_and_users(request: WSGIRequest, id_company: int) -> JsonResponse:
    if request.is_ajax():
        category = request.GET.get('category', None)
        if category is None:
            return JsonResponse({}, status=404)
        company: Company = Company.objects.filter(pk=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)

        search = request.GET.get('search', '')
        if category == 'users':
            content = _load_users(company, get_user_profile(request), search)
        elif category == 'teams':
            content = _load_teams(company, get_user_profile(request), search)
        return JsonResponse({'content': content}, status=200)


def _load_users(company: Company, profile: Profile, search: str):
    # todo search
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


def _load_teams(company: Company, profile: Profile, search: str):
    # todo search
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


def remove_team(request: WSGIRequest, id_company: int, team_id: int):
    if request.is_ajax():
        profile = get_user_profile(request)
        company = profile.company
        if company is None:
            return JsonResponse({}, status=404)
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


def remove_platform(request: WSGIRequest, id_company: int, platform_id: int) -> JsonResponse:
    if request.is_ajax():
        company = Company.objects.filter(pk=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)
        profile = get_user_profile(request)
        if not _profile_is_owner_or_moderator(profile):
            return JsonResponse({}, status=403)
        platform = PlatformCompany.objects.filter(id=platform_id).first()
        if platform is None:
            return JsonResponse({}, status=404)

        platform.delete()
        return JsonResponse({}, status=200)


def save_settings_change(request: WSGIRequest, id_company: int):
    if request.is_ajax():
        profile = get_user_profile(request)
        company_queryset = Company.objects.filter(pk=id_company)
        company = company_queryset.first()
        if company is None:
            return JsonResponse({}, status=404)
        if not _profile_is_owner_or_moderator(profile):
            return JsonResponse({}, status=403)
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name is None or description is None:
            return JsonResponse({}, status=403)
        if not validate_user_input_in_company_settings(name) or not validate_user_input_in_company_settings(description):
            return JsonResponse({}, status=400)

        company_queryset.update(name=name, description=description)
        return JsonResponse({}, status=200)
