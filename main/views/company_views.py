import uuid

from main.forms import CompanyForm
from main.models import Company, PositionCompany, PlatformCompany
from main.views.auxiliary_general_methods import *
from django.shortcuts import render, redirect


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
    return render(request, 'main/companies/add_new_company.html', args)


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


def company_view(request, id_company):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    company = Company.objects.get(id=id_company)

    if company is None:
        return redirect('/communications/')

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
