from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from .forms import ProfileForm, CompanyForm
import copy
from .models import Profile, Company


def user_view(request):
    return render(request, 'main/user.html', {
        "title": "Мой профиль"
    })


def user_view_test(request):
    try:
        user = auth.get_user(request)
        profile_user = Profile.objects.get(user=user)
    except:
        print('Пользователь не авторизирован')
    else:
        print(profile_user.name)
        print(profile_user.surname)

    try:
        company = Company.objects.get(workers=user)
    except:
        print('Нет компании')
    else:
        print(company)
    return redirect('/')


def add_company_test(request):
    args = {}
    if not auth.get_user(request).is_authenticated:
        args['error'] = "Пользователь еще не авторизирован"
        return render(request, 'main/error.html', args)

    args['company_form'] = CompanyForm()
    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company = company_form.save(commit=False)
            user = auth.get_user(request)
            company.owner = user
            company.save()

            profile = Profile.objects.get(user=user)
            profile.company = company
            profile.save()

            return redirect('/')
        else:
            args['company_form'] = company_form
    args['title'] = "Создание компании"
    return render(request, 'main/add_company_test.html', args)


def connect_to_company(request):
    args = {}
    user = auth.get_user(request)
    if not user.is_authenticated:
        args['error'] = "Пользователь еще не авторизирован"
        return render(request, 'main/error.html', args)

    args['company_form'] = CompanyForm()
    if request.method == 'POST':
        try:
            name_company = request.POST.get("name", '')
            company = Company.objects.get(name=name_company)
        except:
            return render(request, 'main/error.html', {'error': "Такой компании не существует"})
        else:
            profile = Profile.objects.get(user=user)
            profile.company = company
            profile.save()
            return redirect('/')
    args['title'] = "Добавление участников"
    return render(request, 'main/connect_to_company.html', args)


def index_view(request):
    return render(request, 'main/index.html', {})


def user_register(request):
    args = {}
    if auth.get_user(request).is_authenticated:
        args['error'] = "Пользователь уже авторизирован"
        return render(request, 'main/error.html', args)

    args['user_form'] = UserCreationForm()
    args['profile_form'] = ProfileForm()
    if request.method == 'POST':

        post = copy.deepcopy(request.POST)
        post['username'] = post['username'].lower()

        user_form = UserCreationForm(post)
        profile_form = ProfileForm(post)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.user = user
            user.save()
            profile.save()

            # Убрать, если не нужна автоматическая авторизация после регистрации пользователя
            auth.login(request, user)

            return redirect('/')
        else:
            args['user_form'] = user_form
            args['profile_form'] = profile_form
    args['title'] = "Регистрация"
    return render(request, 'main/register_test.html', args)


def user_login(request):
    args = {
        "title": "Вход",
    }
    if request.POST:
        username = request.POST.get("username", '').lower()
        password = request.POST.get("password", '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Логин или пароль неверны"
            return render(request, 'main/login.html', args)
    else:
        return render(request, 'main/login.html', args)


def user_logout(request):
    auth.logout(request)
    return redirect('/')


def groups_view(request):
    return render(request, 'main/groups.html', {
        "title": "Группы"
    })
# Create your views here.
