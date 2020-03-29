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


def exception_if_user_not_autinficated(request):
    if not auth.get_user(request).is_authenticated:
        return render(request, 'main/error.html', {'error' "Пользователь еще не авторизирован"})


def change_user_profile_test(request):
    exception_if_user_not_autinficated(request)
    args = {}
    user = auth.get_user(request)
    profile = Profile.objects.get(user=user)
    args['profile_form'] = ProfileForm({
        'name': profile.name,
        'surname': profile.surname,
        'patronymic': profile.patronymic,
        'city': profile.city,
    })
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile.name = request.POST.get('name', '')
            profile.patronymic = request.POST.get('patronymic', '')
            profile.surname = request.POST.get('surname', '')
            profile.city = request.POST.get('city', '')
            profile.save()
            return redirect('/')
    args['title'] = "Редактирование профия"
    return render(request, 'main/change_user_profile.html', args)


def add_company_test(request):
    exception_if_user_not_autinficated(request)

    args = {'company_form': CompanyForm()}
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
    exception_if_user_not_autinficated(request)

    user = auth.get_user(request)
    args = {'company_form': CompanyForm()}
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
    return render(request, 'main/connect_to_company_test.html', args)


def get_all_users_in_company(request):
    exception_if_user_not_autinficated(request)
    user = auth.get_user(request)
    profile = Profile.objects.get(user=user)
    company = profile.company
    users = company.profile_set.all()
    for i in users:
        print(i)
    return redirect('/')


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
