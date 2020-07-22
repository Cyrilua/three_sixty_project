import uuid

from main.forms import CompanyForm
from main.models import Company, PlatformCompany, PositionCompany, PositionCompany, PlatformCompany
from main.views.auxiliary_general_methods import *


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

            return redirect('/')
        else:
            args['company_form'] = company_form
    return render(request, 'main/companies/add_new_company.html', args)


def connect_to_company_to_key(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    args = {'company_form': CompanyForm(),
            'title': "Добавление участников"}

    if profile.company is not None:
        return redirect('/')

    if request.method == 'POST':
        try:
            key_company = request.POST.get("key", '')
            company = Company.objects.get(key=key_company)
        except:
            return redirect('/')
        else:
            add_user_to_company(profile, company)
            return redirect('/')

    return render(request, 'main/companies/connect_to_company.html', args)


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
        return redirect('/')

    try:
        company = Company.objects.get(key=key)
    except:
        return redirect('/')
    else:
        add_user_to_company(profile, company)
        return redirect('/')


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


def company_view(request, id_company):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    company = Company.objects.get(id=id_company)

    if company is None:
        return redirect('/')

    args = {
        'title': company.name,
        'positions': PositionCompany.objects.filter(company=company),
        'platforms': PlatformCompany.objects.filter(company=company),
        'company_name': company.name,
        'owner': {'pk': company.owner.profile.pk,
                  'name': company.owner.profile.name,
                  'surname': company.owner.profile.surname},
        'link_to_enter': request.scheme + "://" + request.get_host() + "/invite/c/" + company.key,
    }

    return render(request, 'main/companies/company_view.html', args)


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
            return redirect('/')
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
        return redirect('/')

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
            return redirect('/')
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
        return redirect('/')
    return render(request, 'main/platform_choice.html', args)


def search_admins(request):
    result = find_user(request,
                       action_with_selected_user='main:add_admin_method',
                       limited_access=True,
                       function_determining_access=determine_access)
    return result


def determine_access(request):
    user = auth.get_user(request)
    company = get_user_profile(request).company
    user_is_admin = user_is_admin_in_current_company(request)
    user_is_owner = user == company.owner
    return user_is_admin or user_is_owner


def add_admins(request, profile_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    company = get_user_profile(request).company
    user_is_owner_current_company = auth.get_user(request) == company.owner
    if user_is_admin_in_current_company(request) or not user_is_owner_current_company:
        return redirect('/')

    profile_new_admin = Profile.objects.get(id=profile_id)
    new_admin = Moderator()
    new_admin.company = company
    new_admin.profile = profile_new_admin
    new_admin.save()
    return redirect('/')


def user_is_admin_in_current_company(request):
    profile = get_user_profile(request)
    try:
        result = Moderator.objects.get(profile=profile).company == profile.company
    except:
        result = False
    return result


def search_hr(request):
    result = find_user(request, action_with_selected_user='main:add_hr_method',
                       limited_access=True,
                       function_determining_access=determine_access)
    return result


def add_hr(request, profile_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    company = get_user_profile(request).company
    user_is_owner_current_company = auth.get_user(request) == company.owner
    if user_is_admin_in_current_company(request) or not user_is_owner_current_company:
        return redirect('/')

    profile_new_hr = Profile.objects.get(id=profile_id)
    new_hr = SurveyWizard()
    new_hr.profile = profile_new_hr
    new_hr.company = company
    new_hr.save()
    return redirect('/')
