import copy
import re
import uuid

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import ProfileForm, CompanyForm, TeamForm, PhotoProfileForm
from .models import Profile, Company, Platforms, Position, Group, Questions, Poll, PositionCompany, PlatformCompany, \
    Answers, ProfilePhoto


def user_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)

    rating = 0
    if profile.count_answers > 0:
        rating = profile.answers_sum / profile.count_answers

    last_poll = profile.last_poll

    args = {
        "title": "Мой профиль",
        'profile': profile,
        'rating': rating,
        'last_poll': last_poll,
    }

    return render(request, 'main/profile.html', args)


def upload_profile_photo(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    args = {
        'title': "Добавление фотографии пользователя",
        'form': PhotoProfileForm()
    }

    if request.method == "POST":
        photo_profile = ProfilePhoto()
        photo_profile.photo = request.FILES['photo']
        photo_profile.profile = profile
        photo_profile.save()
        return redirect('/')
    return render(request, "main/upload_photo.html", args)


def get_photo_test(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    photo = profile.profilephoto.photo
    print("####")
    print(photo)
    print('###')
    return render(request, 'main/test_view_profile_photo.html', {'photo': photo})


def other_user_view(request, profile_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = Profile.objects.get(id=profile_id)
    args = {
        'title': "Профиль просматриваемого пользователя",
        'name': profile.name,
        'surname': profile.surname,
        'patronymic': profile.patronymic,
        'groups': profile.groups.all(),
        'position': profile.position.name,
        'company': profile.company.name,
        'platform': profile.platform.name
    }

    return render(request, "main/other_profile_view.html", args)


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


def edit_profile(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {}
    profile = get_user_profile(request)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile.name = request.POST.get('name', '')
            profile.patronymic = request.POST.get('patronymic', '')
            profile.surname = request.POST.get('surname', '')
            profile.city = request.POST.get('city', '')
            profile.save()
    args['profile_form'] = ProfileForm({
        'name': profile.name,
        'surname': profile.surname,
        'patronymic': profile.patronymic,
        'city': profile.city,
    })
    args['title'] = "Редактирование профия"
    args['profile'] = profile
    return render(request, 'main/edit_profile.html', args)


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


# def index_view(request):
#     args = {}
#     if auth.get_user(request).is_authenticated:
#         args['name'] = get_user_profile(request).name
#     return render(request, 'main/index_old.html', args)


def user_register(request):
    if auth.get_user(request).is_authenticated:
        return redirect('/profile')

    args = {'user_form': UserCreationForm(),
            'profile_form': ProfileForm(),
            'title': "Регистрация"}

    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post['username'] = post['username'].lower()
        user_form = UserCreationForm(post)
        profile_form = ProfileForm(post)

        if user_form.is_valid() and profile_form.is_valid():
            print(request.POST.get('username', ''))
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
    return render(request, 'main/register.html', args)


def user_login(request):
    if auth.get_user(request).is_authenticated:
        return redirect('/profile')

    args = {'title': "Вход"}

    if request.POST:
        username = request.POST.get("username", '').lower()
        password = request.POST.get("password", '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/profile')
        else:
            args['login_error'] = "Неверный логин или пароль"
            args['username'] = username
            return render(request, 'main/login.html', args)
    return render(request, 'main/login.html', args)


def user_logout(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    auth.logout(request)
    return redirect('/')


def create_team(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {
        'title': 'Создание новой группы',
        'team_form': TeamForm()
    }

    user = auth.get_user(request)
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        team_form = TeamForm(request.POST)

        if team_form.is_valid():
            new_team = team_form.save(commit=False)
            new_team.owner = user
            new_team.key = uuid.uuid4().__str__()
            new_team.save()

            profile.groups.add(new_team)
            profile.groups.add()
        return redirect('/communications/')
    return render(request, 'main/add_new_team.html', args)


def connect_to_team(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {'title': 'Присоединиться к комманде'}
    profile = get_user_profile(request)

    if request.method == "POST":
        try:
            key_group = request.POST.get('key', '')
            group = Group.objects.get(key=key_group)
            if group in profile.groups.all():
                args['error'] = "Пользователь уже состоит в этой команде"
                return render(request, 'main/connect_to_team.html', args)
        except:
            args['error'] = "Ключ не существует или введен неверно"
            return render(request, 'main/connect_to_team.html', args)
        else:
            profile.groups.add(group)
            profile.save()
            return redirect('/communications/')
    return render(request, 'main/connect_to_team.html', args)


def teams_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    profile = get_user_profile(request)
    teams = profile.groups.all()
    ### для отладки
    for i in teams:
        print(i)
        users = i.profile_set.all()
        for j in users:
            print('    ' + j.__str__())
    ####
    return render(request, 'main/communications.html', {
        'title': "Группы",
        'teams': teams,
        'profile': profile,
    })


def team_user_view(request, group_id):
    args = {'title': "Просмотр пользователей группы"}

    if auth.get_user(request).is_anonymous:
        return redirect('/')
    try:
        group = Group.objects.get(id=group_id)
    except:
        args['error'] = "Данной группы не существует"
        return render(request, 'main/group_user.html', args)

    args['users'] = group.profile_set.all()
    return render(request, 'main/group_user.html', args)


def add_new_question(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {'title': "Добавить новый вопрос"}

    if request.method == "POST":
        new_question = clear_request(request.POST.get('question', '')).lower()
        try:
           Questions.objecte.get(question=new_question)
        except:
            question = Questions(question=new_question)
            question.save()
            #TODO Перенаправлять на нужную страницу
            return redirect('/')
        else:
            args['title'] = "Вопрос уже существует"
            return render(request, 'main/new_question.html', args)
    return render(request, 'main/new_question.html', args)


def find_question(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {'title': "Поиск вопроса"}

    if request.method == "POST":
        required_question = request.POST.get('question', '')
        question = clear_request(required_question)
        result = find_result(question)
        args['questions'] = result
        return render(request, 'main/questions_search.html', args)
    return render(request, 'main/questions_search.html', args)


def clear_request(question):
    new_s = re.sub('[^a-zA-Zа-яА-Я 0-9]+', '', question)
    return new_s


def find_result(question):
    # Не смог сделать уже реализованные решения, написал свое.
    # Потом, скорее всего, будет более оптимальное
    question = question.split(' ')
    temp_result = []
    base_questions = Questions.objects.all()
    for ques in base_questions:
        number_matches = 0
        split_base_ques = ques.question.split()
        for i in question:
            if i in split_base_ques:
                number_matches += 1
        if number_matches > 0:
            temp_result.append((number_matches, ques.id))
    temp_result.sort()
    result = [Questions.objects.get(id=i[1]) for i in temp_result]
    return result


def poll_view(request, pool_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
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
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    user = auth.get_user(request)
    poll = Poll()
    poll.initiator = user
    poll.save()
    id = str(poll.id)
    #Должна будет перенаправляться на страницу выбора списка вопросов
    return redirect('/{}/add_question'.format(id))


def add_questions_in_poll(request, pool_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {'title': "Добавление вопроса в опрос"}
    if request.method == 'POST':
        try:
            poll = Poll.objects.get(id=pool_id)
        except:
            #return render(request, 'main/error.html', {'error': 'Данного опроса не существует'})
            return redirect('/')
        question_id = request.POST.get('question', '')
        try:
            question = Questions.objects.get(id=question_id)
        except:
            args['error'] = 'Данного вопроса не существует'
            #return render(request, 'main/error.html', {'error': 'Данного вопроса не существует'})
            return render(request, 'main/add_question_in_poll.html', args)
        question.poll_set.add(poll)
        return redirect('/')
    return render(request, 'main/add_question_in_poll.html', args)


def add_answer(request, poll_id, question_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {'title': "Ответ на вопрос опроса"}
    try:
        poll = Poll.objects.get(id=poll_id)
    except:
        return redirect('/')

    try:
        question = Questions.objects.get(id=question_id)
    except:
        args['error'] = "Данного вопроса не существует"
        return render(request, 'main/add_answer.html', args)

    if request.method == "POST":
        try:
            answer_user = int(request.POST.get('answer', ''))
        except:
            args['error'] = "Ответ должен быть числом"
            return render(request, 'main/add_answer.html', args)

        #При оценке по 10-ти бальной шкале
        if answer_user > 10 or answer_user < 0:
            args['error'] = "Ответ должен быть числом от 0 до 10"
            return render(request, 'main/add_answer.html', args)

        answer = Answers()
        answer.question = question
        answer.answer = answer_user
        answer.poll = poll
        answer.save()

        profile = get_user_profile(request)
        profile.answers_sum += answer_user
        profile.count_answers += 1
        profile.save()

        #Временно, не знаю куда отправлять
        return redirect('/')
    return render(request, 'main/add_answer.html', args)


def questions_in_pool_view(request, poll_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {'title': "Ответ на вопрос опроса"}
    try:
        poll = Poll.objects.get(id=poll_id)
    except:
        return redirect('/')

    questions = Questions.objects.filter(poll=poll)
    args['questions'] = questions
    for i in questions:
        print(i)
    return render(request, 'main/poll_questions.html', args)
# Create your views here.
