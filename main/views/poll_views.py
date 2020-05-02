from django.shortcuts import redirect
from django.shortcuts import render

from main.models import Questions, Poll, Answers, CompanyHR
from main.views.auxiliary_general_methods import *


def type_poll(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    return render(request, 'main/type_poll.html', {'title': 'Выбор типа опроса'})


def default_poll_template_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    polls = Poll.objects.filter(template_type=0)
    try:
        is_hr = CompanyHR.objects.get(profile=get_user_profile(request)) is not None
    except:
        is_hr = False
    args = {
        'title': 'Список опросов',
        'polls': polls,
        'access': is_hr
    }
    return render(request, 'main/default_polls.html', args)


def search_target_poll(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    result = find_user(request,
                       action_with_selected_user='main:select_survey_area',
                       limited_access=True,
                       function_determining_access=user_is_hr_or_owner)
    return result


def user_is_hr_or_owner(request):
    user = auth.get_user(request)
    profile = get_user_profile(request)
    try:
        user_is_hr = CompanyHR.objects.get(profile=profile) is not None
    except:
        user_is_hr = False
    user_is_owner = profile.company.owner.id == user.id
    return user_is_owner or user_is_hr


def select_survey_area(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    return redirect('/')


def poll_view(request, pool_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    poll = Poll.objects.get(id=pool_id)
    user_auth = auth.get_user(request)
    user_init = poll.initiator
    questions = Questions.objects.filter(poll=poll)
    if user_auth.username == user_init.username:
        # TODO
        return render(request, 'main.error_old.html', {'error': "Вывод описания опроса"})
    else:
        return render(request, 'main.error_old.html', {'error': "У вас пользователя прав для редактирования опроса"})


def create_pool(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    user = auth.get_user(request)
    poll = Poll()
    poll.initiator = user
    poll.save()
    id = str(poll.id)
    # Должна будет перенаправляться на страницу выбора списка вопросов
    return redirect('/{}/add_question'.format(id))


def add_questions_in_poll(request, pool_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {'title': "Добавление вопроса в опрос"}
    if request.method == 'POST':
        try:
            poll = Poll.objects.get(id=pool_id)
        except:
            # return render(request, 'main/error_old.html', {'error': 'Данного опроса не существует'})
            return redirect('/')
        question_id = request.POST.get('question', '')
        try:
            question = Questions.objects.get(id=question_id)
        except:
            args['error'] = 'Данного вопроса не существует'
            # return render(request, 'main/error_old.html', {'error': 'Данного вопроса не существует'})
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

        # При оценке по 10-ти бальной шкале
        if answer_user > 10 or answer_user < 0:
            args['error'] = "Ответ должен быть числом от 0 до 10"
            return render(request, 'main/add_answer.html', args)

        answer = Answers()
        answer.question = question
        answer.sum_answer = answer_user
        answer.poll = poll
        answer.save()

        profile = get_user_profile(request)
        profile.answers_sum += answer_user
        profile.count_answers += 1
        profile.save()

        # Временно, не знаю куда отправлять
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


def answer_the_poll(request, poll_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        poll = Poll.objects.get(id=poll_id)
    except:
        return redirect('/')

    args = {'title': 'Прохождение опроса',
            'questions': poll.questions.all()}

    # Закомментированно на время разработки
    if not user_is_respondent(request, poll):
        # TODO Если текущий пользователь прошел опрос или его нет в списке опрашиваемых
        # return redirect('/')
        pass

    for i in args['questions']:
        print(i)

    if request.method == "POST":
        for question in args['questions']:
            # Создание объекта ответа
            user_answer = int(request.POST.get('answer-{}'.format(question.id)))
            try:
                change_answer = Answers.objects.get(question=question)
            except:
                # TODO создавать ответы во время создания опроса
                change_answer = Answers()
                change_answer.poll = poll
                change_answer.question = question
            change_answer.sum_answer += user_answer
            change_answer.count_answers += 1
            change_answer.save()

        # Удаление прошедшего опрос пользователя
        poll.respondents.remove(auth.get_user(request))
        poll.save()

        if len(poll.respondents.all()) == 0:
            # TODO
            print("Обработка результата, когда все опрашиваемые прошли опрос")
        return redirect('/')

    return render(request, 'main/poll/answer_the_poll.html', args)


def user_is_respondent(request, poll):
    respondents = poll.respondents.all()
    user = auth.get_user(request)
    count_users = len(list(filter(lambda x: x.id == user.id, respondents)))
    return count_users == 1


def result_view(request, poll_id):
    # Использоется как для вывода конечного результата опроса
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        poll = Poll.objects.get(id=poll_id)
    except:
        return redirect('/')

    if poll.initiator.id != auth.get_user(request).id:
        return redirect('/')

    # Словарь (ключ - вопрос, значение - средний ответ)
    question_by_answer_result = calculate_result_questions(poll.questions.all())
    args = {
        'title': 'Получение результатов опроса',
        'results': question_by_answer_result
    }
    return render(request, 'main/result_poll.html', args)


def calculate_result_questions(questions):
    question_by_answer_result = {}
    for question in questions:
        answer = Answers.objects.get(question=question)
        question_by_answer_result[question] = answer.sum_answer / answer.count_answers
    return question_by_answer_result


def new_poll(request):
    args = {}
    return render(request, 'main/poll/new_poll.html', args)
