from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth

from .forms import ProfileForm, CompanyForm
import copy, uuid
from .models import Profile, Company, Platforms, Position, Group, Questions, Poll
import re


def user_view(request):
    # Раскомментировать, после разработки
    # error = exception_if_user_not_autinficated(request)
    # if error is not None:
    #     return error
    args = {"title": "Мой профиль"}
    if auth.get_user(request).is_authenticated:
        args['profile'] = get_user_profile(request)
    return render(request, 'main/user.html', args)


def exception_if_user_not_autinficated(request):
    if not auth.get_user(request).is_authenticated:
        return render(request, 'main/error.html', {'error': "Пользователь еще не авторизирован",
                                                   'title': "Ошибка"})


def exception_if_user_autinficated(request):
    if auth.get_user(request).is_authenticated:
        return render(request, 'main/error.html', {'error': "Пользователь уже авторизирован",
                                                   'title': "Ошибка"})


def get_user_profile(request):
    user = auth.get_user(request)
    return Profile.objects.get(user=user)


def change_user_profile_test(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    args = {}
    profile = get_user_profile(request)
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


def add_new_platform(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    if request.method == "POST":
        new_platform = request.POST.get("platform", '').lower()
        try:
            Platforms.objects.get(name=new_platform)
        except:
            platform = Platforms(name=new_platform)
            platform.save()
            return redirect('/')
        else:
            return render(request, 'main/error.html', {'error': "Эта платформа уже существует",
                                                       'title': "Ошибка"})
    return render(request, 'main/add_new_platform.html', {'title': 'Добавление новой платформы'})


def add_new_position(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    if request.method == "POST":
        new_position = request.POST.get("position", '').lower()
        try:
            Position.objects.get(name=new_position)
        except:
            position = Position(name=new_position)
            position.save()
            return redirect('/')
        else:
            return render(request, 'main/error.html', {'error': "Эта должность уже существует",
                                                       'title': "Ошибка"})
    return render(request, 'main/add_new_position.html', {'title': 'Добавление новой должности'})


def add_company_test(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error

    args = {'company_form': CompanyForm()}
    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company = company_form.save(commit=False)
            user = auth.get_user(request)
            company.owner = user
            company.key = uuid.uuid4().__str__()
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
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error

    profile = get_user_profile(request)
    args = {'company_form': CompanyForm()}
    if request.method == 'POST':
        try:
            key_company = request.POST.get("key", '')
            company = Company.objects.get(key=key_company)
        except:
            return render(request, 'main/error.html', {'error': "Ключ не существует или введен неверно"})
        else:
            if profile.company is not None:
                return render(request, 'main/error.html', {'error': "Данный пользователь уже состоит в компании"})
            profile.company = company
            profile.save()
            return redirect('/')
    args['title'] = "Добавление участников"
    return render(request, 'main/connect_to_company_test.html', args)


def get_all_users_in_company(request):
    exception_if_user_not_autinficated(request)
    profile = get_user_profile(request)
    company = profile.company
    try:
        users = company.profile_set.all()
    except:
        return render(request, 'main/error.html', {'error': "Пользователь не состоит в компании",
                                                   'title': "Ошибка"})
    else:
        # return render(request, 'main/some_file.html', {'users': users})
        return redirect('/')


def index_view(request):
    args = {}
    if auth.get_user(request).is_authenticated:
        args['name'] = get_user_profile(request).name
    return render(request, 'main/index.html', args)


def user_register(request):
    error = exception_if_user_autinficated(request)
    if error is not None:
        return error
    args = {'user_form': UserCreationForm(), 'profile_form': ProfileForm()}
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
    error = exception_if_user_autinficated(request)
    if error is not None:
        return error
    args = {'title': "Вход"}
    if request.POST:
        username = request.POST.get("username", '').lower()
        password = request.POST.get("password", '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Неверный логин или пароль"
            args['username'] = username
            return render(request, 'main/login.html', args)
    return render(request, 'main/login.html', args)


def user_logout(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    auth.logout(request)
    return redirect('/')


def create_group(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    user = auth.get_user(request)
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        new_group_name = request.POST.get('name_company', '')
        new_group = Group(
            name=new_group_name,
            owner=user,
            key=uuid.uuid4().__str__()
        )
        new_group.save()

        profile.groups.add(new_group)
        profile.groups.add()
        # Не плохо было бы сразу направлять на страницу группы
        return redirect('/')
    return render(request, 'main/create_group.html', {'title': 'Создание новой группы'})


def connect_to_group(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    profile = get_user_profile(request)
    if request.method == "POST":
        try:
            key_group = request.POST.get('key', '')
            group = Group.objects.get(key=key_group)
        except:
            return render(request, 'main/error.html', {'error': "Ключ не существует или введен неверно"})
        else:
            profile.groups.add(group)
            profile.save()
            return redirect('/')
    return render(request, 'main/connect_to_group.html', {'title': 'Присоединиться к группе'})


def groups_view(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    profile = get_user_profile(request)
    groups = profile.groups.all()
    ### для отладки
    for i in groups:
        print(i)
        users = i.profile_set.all()
        for j in users:
            print('    ' + j.__str__())
    ####
    return render(request, 'main/groups.html', {
        "title": "Группы",
        'groups': groups,
    })


def add_new_question(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    if request.method == "POST":
        new_question = request.POST.get('question', '').lower()
        try:
            question = Questions.objecte.get(question=new_question)
        except:
            question = Questions(question=new_question)
            question.save()
        else:
            return render(request, 'main/error.html', {'error': "Вопрос уже существует"})
    return render(request, 'main/new_question', {'title': "Добавить новый вопрос"})


def find_question(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    if request.method == "POST":
        required_question = request.POST.get('question', '')
        clear_request = clear_find_request(required_question)
        result = find_result(clear_request)
        return render(request, 'main/find_questions.html', {
            'title': "Поиск вопроса",
            'questions': result
        })
    return render(request, 'main/find_questions.html', {'title': "Поиск вопроса"})


def clear_find_request(question):
    new_s = re.sub('[^a-zA-Zа-яА-Я 0-9]+', '', question)
    return new_s


def find_result(question):
    # Не смог сделать уже реализованные решения, написал свое.
    # Потом, скорее всего, будет более оптимальное
    questions = []
    base_questions = Questions.objects.all()
    for base_num in range(len(base_questions)):
        temp_result = 0
        for i in question:
            base_question = base_questions[base_num].question.split()
            if i in base_question:
                temp_result += 1
        questions.append((temp_result, base_num))
    questions.sort()
    result = []
    number_questions = 10
    for i in range(number_questions):
        position = len(questions) - i - 1
        result.append(base_questions[questions[position][1]].question)
    return result


def poll_view(request, pool_id):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    poll = Poll.objects.get(id=pool_id)
    user_auth = auth.get_user(request)
    user_init = poll.initiator
    questions = Questions.objects.filter(poll=poll)
    if user_auth.username == user_init.username:
        #TODO
        return render(request, 'main.error.html', {'error': "Вывод описания опроса"})
    else:
        return render(request, 'main.error.html', {'error': "У вас пользователя прав для редактирования опроса"})


def create_pool(request):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    user = auth.get_user(request)
    poll = Poll()
    poll.initiator = user
    poll.save()
    id = str(poll.id)
    #Должна будет перенаправляться на страницу выбора списка вопросов
    return redirect(id + '/add_question')


def add_questions_in_pool(request, pool_id):
    error = exception_if_user_not_autinficated(request)
    if error is not None:
        return error
    if request.method == 'POST':
        try:
            poll = Poll.objects.get(id=pool_id)
        except:
            return render(request, 'main/error.html', {'error': 'Данного опроса не существует'})
        question_id = request.POST.get('question', '')
        try:
            question = Questions.objects.get(id=question_id)
        except:
            return render(request, 'main/error.html', {'error': 'Данного вопроса не существует'})
        question.poll_set.add(poll)
        return redirect('/')
    return render(request, 'main/add_question_in_poll.html', {'title': "Добавление вопроса в опрос"})

# Create your views here.
