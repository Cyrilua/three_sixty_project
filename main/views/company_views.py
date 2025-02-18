from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.response import SimpleTemplateResponse

from main.models import ProfilePhoto, SurveyWizard, Moderator, Group, NeedPassPoll, Poll
from main.views.auxiliary_general_methods import *
from .validators import validate_user_input_in_company_settings


def create_company(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    company = Company()
    company.owner = profile
    company.name = "Новая компания"
    company.description = "описание компании"
    company.save()
    _create_unique_key(company)

    profile.company = company
    profile.save()

    return redirect('/company/{}/'.format(company.pk))


def _create_unique_key(company: Company):
    team_id_changed = company.pk % 1000 + 1000
    owner_id_changed = company.owner.pk % 1000 + 1000
    date_now = datetime.today()
    date_changed_str = '{}{}{}{}{}{}{}'.format(date_now.day, date_now.month,
                                               date_now.year, date_now.hour, date_now.minute, date_now.second, date_now.microsecond)
    key = '{}{}{}'.format(team_id_changed, owner_id_changed, date_changed_str)
    company.key = key
    company.save()


def redirect_create_poll(request: WSGIRequest, id_company: int):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    return redirect('/poll/editor/company/{}/new/'.format(id_company))


def company_view(request: WSGIRequest, id_company: int):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.method == "GET":
        company: Company = Company.objects.filter(pk=id_company).first()
        if company is None:
            return render(request, 'main/errors/global_error.html', {'global_error': '404'})

        profile = get_user_profile(request)
        if profile.company is None or profile.company != company:
            return render(request, 'main/errors/global_error.html', {'global_error': '403'})

        args = {
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
        args['profile']['is_moderator'] = Moderator.objects.filter(profile=profile).exists()
        print(args)
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
    profiles = company.profile_set.all()
    if search != '':
        profiles = get_search_result_for_profiles(profiles, search, company)
    collected_profiles = _build_profiles(profiles, profile)
    if len(collected_profiles) == 0:
        content = get_render_bad_search('По вашему запросу ничего не найдено')
    else:
        args = {
            'users': collected_profiles,
            'profile': {
                'is_boss': company.owner == profile,
                'is_moderator': Moderator.objects.filter(profile=profile).exists()
            }
        }
        content = SimpleTemplateResponse('main/companies/users.html', args).rendered_content
    return content


def _build_profiles(profiles: list, current_profile: Profile):
    result = []
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
            'new_roles': _get_new_roles(profile, current_profile),
            'positions': profile.positions.all(),
            'new_positions': PositionCompany.objects.filter(company=profile.company).exclude(profile=profile),
            'platforms': profile.platforms.all(),
            'new_platforms': PlatformCompany.objects.filter(company=profile.company).exclude(profile=profile),
            'is_boss': profile.company.owner == profile
        }
        result.append(collected_profile)
    return result


def _load_teams(company: Company, profile: Profile, search: str):
    teams = Group.objects.filter(company=company)
    if search != '':
        teams = get_search_result_for_teams(teams, search)
    collected_teams = []
    for team in teams:
        team: Group
        collected_teams.append({
            'id': team.pk,
            'href': '/team/{}/'.format(team.pk),
            'name': team.name,
            'quantity': team.profile_set.all().count(),
            'description': team.description,
        })
    if len(collected_teams) == 0:
        content = get_render_bad_search('По вашему запросу ничего не найдено')
    else:
        args = {
            'teams': collected_teams,
            'profile': {
                'is_boss': company.owner == profile,
                'is_moderator': Moderator.objects.filter(profile=profile).exists()
            }
        }
        content = SimpleTemplateResponse('main/companies/teams.html', args).rendered_content
    return content


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
            return render(request, 'main/errors/global_error.html', {'global_error': '404'})
        args = {
            'company': {
                'name': company.name,
                'description': company.description,
                'hrefForInvite': ''.join(['http://', get_current_site(request).domain, '/company/{}/'.format(company.pk),
                                          'invite_company/', company.key]),
                'positions': PositionCompany.objects.filter(company=company),
                'platforms': PlatformCompany.objects.filter(company=company),
                'countParticipants': company.profile_set.all().count(),
                'countTeams': Group.objects.filter(company=company).count()
            },
            'profile': get_header_profile(profile)
        }
        args['profile']['is_boss'] = company.owner == profile
        args['profile']['is_moderator'] = Moderator.objects.filter(profile=profile).exists()
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


def _get_new_roles(profile: Profile, current_profile) -> list:
    roles = []
    if current_profile.company is None:
        return roles
    if not SurveyWizard.objects.filter(profile=profile).exists():
        roles.append('master')
    if not Moderator.objects.filter(profile=profile).exists() and current_profile.company.owner == current_profile:
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
        return JsonResponse({'positionId': position.pk}, status=200)


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
        return JsonResponse({'platformId': platform.pk}, status=200)


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
        name = request.POST.get('name', company.name)
        description = request.POST.get('description', company.description)
        if name is None or description is None:
            return JsonResponse({}, status=403)
        if not validate_user_input_in_company_settings(name) or \
                not validate_user_input_in_company_settings(description):
            return JsonResponse({}, status=400)

        company_queryset.update(name=name, description=description)
        return JsonResponse({}, status=200)


def assign_role_profile(request: WSGIRequest, id_company: int, profile_id: int) -> JsonResponse:
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        company = Company.objects.filter(id=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)

        changed_profile_role = Profile.objects.filter(id=profile_id).first()
        if changed_profile_role is None:
            return JsonResponse({}, status=404)

        current_profile = get_user_profile(request)

        role = request.POST.get('roleName', '')
        if role == 'master':
            if current_profile != company.owner and not Moderator.objects.filter(profile=current_profile).exists():
                return JsonResponse({}, status=403)
            if SurveyWizard.objects.filter(profile=changed_profile_role).exists():
                return JsonResponse({}, status=400)
            new_master = SurveyWizard()
            new_master.profile = changed_profile_role
            new_master.company = company
            new_master.save()
        elif role == 'moderator':
            if current_profile != company.owner or Moderator.objects.filter(profile=changed_profile_role).exists():
                return JsonResponse({}, status=403)
            new_moderator = Moderator()
            new_moderator.profile = changed_profile_role
            new_moderator.company = company
            new_moderator.save()
        else:
            return JsonResponse({}, status=400)
        return JsonResponse({}, status=200)


def remove_role_from_profile(request: WSGIRequest, id_company: int, profile_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        current_profile = get_user_profile(request)
        company = Company.objects.filter(id=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)

        changed_profile_role = Profile.objects.filter(id=profile_id).first()
        if changed_profile_role is None:
            return JsonResponse({}, status=404)

        role_name = request.POST.get('roleName', '')
        if role_name == 'master':
            if not _profile_is_owner_or_moderator(current_profile):
                return JsonResponse({}, status=403)

            SurveyWizard.objects.filter(profile=changed_profile_role).delete()

        elif role_name == 'moderator':
            if current_profile != company.owner:
                return JsonResponse({}, status=403)

            Moderator.objects.filter(profile=changed_profile_role).delete()

        else:
            return JsonResponse({}, status=404)

        return JsonResponse({}, status=200)


def join_company_from_link(request: WSGIRequest, id_company: int, key: str):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    company = Company.objects.filter(id=id_company).first()
    if company is None or key != company.key:
        return render(request, 'main/errors/global_error.html', {'global_error': '404'})

    profile = get_user_profile(request)
    if profile.company is not None:
        return render(request, 'main/errors/global_error.html', {'global_error': '403'})

    profile.company = company
    profile.save()
    return redirect('/company/{}/'.format(company.pk))


def assign_position_profile(request: WSGIRequest, id_company: int, profile_id: int, position_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        current_profile = get_user_profile(request)
        if not _profile_is_owner_or_moderator(current_profile):
            return JsonResponse({}, status=403)

        company = Company.objects.filter(id=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)

        changed_profile: Profile = Profile.objects.filter(id=profile_id).first()
        if changed_profile is None:
            return JsonResponse({}, status=404)

        added_position = PositionCompany.objects.filter(id=position_id).first()
        if added_position is None:
            return JsonResponse({}, status=404)

        changed_profile.positions.add(added_position)
        return JsonResponse({}, status=200)


def remove_position_profile(request: WSGIRequest, id_company: int, profile_id: int, position_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        current_profile = get_user_profile(request)
        if not _profile_is_owner_or_moderator(current_profile):
            return JsonResponse({}, status=403)

        company = Company.objects.filter(id=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)

        changed_profile: Profile = Profile.objects.filter(id=profile_id).first()
        if changed_profile is None:
            return JsonResponse({}, status=404)

        removed_position = PositionCompany.objects.filter(id=position_id).first()
        if removed_position is None:
            return JsonResponse({}, status=404)

        changed_profile.positions.remove(removed_position)
        return JsonResponse({}, status=200)


def assign_platform_profile(request: WSGIRequest, id_company: int, profile_id: int, platform_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        current_profile = get_user_profile(request)
        if not _profile_is_owner_or_moderator(current_profile):
            return JsonResponse({}, status=403)

        company = Company.objects.filter(id=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)

        changed_profile: Profile = Profile.objects.filter(id=profile_id).first()
        if changed_profile is None:
            return JsonResponse({}, status=404)

        added_platform = PlatformCompany.objects.filter(id=platform_id).first()
        if added_platform is None:
            return JsonResponse({}, status=404)

        changed_profile.platforms.add(added_platform)
        return JsonResponse({}, status=200)


def remove_platform_profile(request: WSGIRequest, id_company: int, profile_id: int, platform_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        current_profile = get_user_profile(request)
        if not _profile_is_owner_or_moderator(current_profile):
            return JsonResponse({}, status=403)

        company = Company.objects.filter(id=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)

        changed_profile: Profile = Profile.objects.filter(id=profile_id).first()
        if changed_profile is None:
            return JsonResponse({}, status=404)

        added_platform = PlatformCompany.objects.filter(id=platform_id).first()
        if added_platform is None:
            return JsonResponse({}, status=404)

        changed_profile.platforms.remove(added_platform)
        return JsonResponse({}, status=200)


def kick_profile_from_company(request: WSGIRequest, id_company: int, profile_id: int):
    if request.is_ajax():
        if auth.get_user(request).is_anonymous:
            return JsonResponse({}, status=404)

        current_profile = get_user_profile(request)
        if not _profile_is_owner_or_moderator(current_profile):
            return JsonResponse({}, status=403)

        company = Company.objects.filter(id=id_company).first()
        if company is None:
            return JsonResponse({}, status=404)

        changed_profile = Profile.objects.filter(id=profile_id).first()
        if changed_profile is None:
            return JsonResponse({}, status=404)

        changed_profile.platforms.clear()
        changed_profile.positions.clear()
        company.profile_set.remove(changed_profile)
        teams = Group.objects.filter(company=company, profile=changed_profile)
        for team in teams:
            if team.owner != changed_profile:
                team.profile_set.remove(changed_profile)
            else:
                team.delete()
        SurveyWizard.objects.filter(profile=changed_profile).delete()
        Moderator.objects.filter(profile=changed_profile).delete()
        NeedPassPoll.objects.filter(profile=changed_profile).delete()
        Poll.objects.filter(target=changed_profile).delete()
        return JsonResponse({}, status=200)


def get_invite_link(request, id_company):
    if request.is_ajax():
        try:
            company = Company.objects.filter(id=int(id_company)).first()
        except ValueError:
            return JsonResponse({}, status=400)

        if company is None:
            return JsonResponse({}, status=404)

        return JsonResponse({'link': '/company/{}/''invite_company/{}'.format(company.pk, company.key)})
