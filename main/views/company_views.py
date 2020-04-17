import uuid

from django.shortcuts import redirect
from django.shortcuts import render

from main.forms import CompanyForm
from main.models import Company, Platforms, Position, PositionCompany, PlatformCompany
from main.views.auxiliary_general_methods import *


def add_new_platform(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {'title': 'Добавление новой платформы'}
    if request.method == "POST":
        new_platform = request.POST.get("platform", '').lower()
        try:
            Platforms.objects.get(name=new_platform)
        except:
            platform = Platforms(name=new_platform)
            platform.save()
            return redirect('/')
        else:
            args['error'] = "Эта платформа уже существует"
            return render(request, 'main/add_new_platform.html', args)
    return render(request, 'main/add_new_platform.html', args)


def add_new_position(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {'title': 'Добавление новой должности'}
    if request.method == "POST":
        new_position = request.POST.get("position", '').lower()
        try:
            Position.objects.get(name=new_position)
        except:
            position = Position(name=new_position)
            position.save()
            return redirect('/')
        else:
            args['error'] = "Эта должность уже существует"
            return render(request, 'main/add_new_position.html', args)
    return render(request, 'main/add_new_position.html', args)


def add_company(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    user = auth.get_user(request)
    profile = Profile.objects.get(user=user)

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
    return render(request, 'main/add_new_company.html', args)


def connect_to_company(request):
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
            return render(request, 'main/connect_to_company.html', {'error': "Ключ не существует или введен неверно"})
        else:
            profile.company = company
            profile.save()
            return redirect('/communications/')
    return render(request, 'main/connect_to_company.html', args)


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

    if request.method == "POST":
        position_name = request.POST.get('position', '')
        try:
            position = Position.objects.get(name=position_name)
        except:
            position = Position(name=position_name)
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
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {'title': "Добавление платформы в компанию"}
    profile = get_user_profile(request)
    company = profile.company

    if company is None:
        args['error'] = "Пользователь не состоит в компании"
        return render(request, 'main/add_new_platform.html', args)

    if request.method == "POST":
        platform_name = request.POST.get('platform', '')
        try:
            platform = Position.objects.get(name=platform_name)
        except:
            platform = Platforms(name=platform_name)
            platform.save()

        platforms_in_company = PlatformCompany.objects.filter(company=company)
        for i in platforms_in_company:
            if i.position.id == platform.id:
                args['error'] = "Эта платформа уже выбрана для этой компании"
                return render(request, 'main/add_new_platform.html', args)

        platform_in_company = PlatformCompany()
        platform_in_company.platform = platform
        platform_in_company.company = company
        platform_in_company.save()

        return redirect('/')
    return render(request, 'main/add_new_platform.html', args)


def company_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    company = profile.company

    if company is None:
        return redirect('/communications/')

    args = {
        'title': "Просмотр компании",
        'positions': PositionCompany.objects.filter(company=company),
        'platform': PlatformCompany.objects.filter(company=company),
        'name': company.name,
        'owner': company.owner,
        'key': company.key,
    }

    return render(request, 'main/company_view.html', args)
