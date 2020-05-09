import uuid

from main.models import Questions, Poll, Answers, CompanyHR, AnswerChoice, Settings
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
            'poll_name': poll.name_poll,
            'questions': build_questions(poll)}

    if poll.description is not None:
        args['about_poll'] = poll.description

    # Закомментированно на время разработки
    if not user_is_respondent(request, poll):
        # TODO Если текущий пользователь прошел опрос или его нет в списке опрашиваемых
        # return redirect('/')
        pass

    if request.method == "POST":
        questions_list = poll.questions.all()
        for question in questions_list:
            change_answer = Answers.objects.get(question=question)
            if question.type == 'checkbox' or question.type == 'radio':
                user_choices_list = [AnswerChoice.objects.get(id=int(i)) for i in
                                     request.POST.getlist('answer-{}'.format(question.id))]
                for choice in user_choices_list:
                    choice.count += 1
                    choice.save()
            elif question.type == 'range':
                user_answer = int(request.POST.get('answer-{}'.format(question.id)))
                change_answer.sum_answer += user_answer
                change_answer.count_answers += 1
            else:
                user_answer = request.POST.get('answer-{}'.format(question.id))
                change_answer.text_answer = user_answer
            change_answer.save()

        # Удаление прошедшего опрос пользователя
        poll.respondents.remove(auth.get_user(request))
        poll.save()

        if len(poll.respondents.all()) == 0:
            # TODO
            print("Обработка результата, когда все опрашиваемые прошли опрос")
        return redirect('/')

    return render(request, 'main/poll/answer_the_poll.html', args)


def build_questions(poll):
    questions_list = poll.questions.all()
    result_questions = []
    for question in questions_list:
        settings = question.settings
        answers_choices = settings.answer_choice.all()
        question = {
            'id': question.id,
            'type': question.type,
            'text': question.text,
            'settings': settings,
            'answers': answers_choices
        }
        result_questions.append(question)
    return result_questions


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

    question_by_answer_result = calculate_result_questions(poll.questions.all())
    args = {
        'title': 'Получение результатов опроса',
        'results': question_by_answer_result
    }
    return render(request, 'main/poll/poll_results.html', args)


def calculate_result_questions(questions):
    results = []
    id = 0
    for question in questions:
        result_question = {
            'type': question.type,
            'text': question.text,
            'id': id
        }
        id += 1
        result_answers = []
        answer = question.answers


        result = {
            'question': result_question,
            'answers': result_answers
        }
    return results


def new_poll(request):
    args = {'title': "Создание опроса"}
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    if request.method == "POST":
        numbers_questions = [int(i) for i in request.POST.get('allQuestionNumbers', '').split(',')]
        poll = create_new_poll(request)
        if len(numbers_questions) > 0:
            create_polls_questions(request, poll, numbers_questions)
    return render(request, 'main/poll/new_poll.html', args)


def create_new_poll(request):
    result = Poll()
    result.key = uuid.uuid4().__str__()

    name_poll = request.POST.get('pollName', '')
    if name_poll is not None and name_poll != '':
        result.name_poll = name_poll
    else:
        result.name_poll = 'Опрос'

    description_poll = request.POST.get('pollAbout', '')
    if description_poll is not None and description_poll != '':
        result.description = description_poll
    else:
        result.description = None
    result.initiator = auth.get_user(request)
    result.save()
    return result


def create_polls_questions(request, poll, numbers_questions):
    for number in numbers_questions:
        question = create_question(request, number)
        count_answer_choice = int(request.POST.get('countOption-{}'.format(number), ''))
        if count_answer_choice > 0:
            create_answers_choices(request, question, number)
        create_answer(question, poll)
        poll.questions.add(question)


def create_question(request, number_question):
    question = Questions()
    type_question = request.POST.get('questionType-{}'.format(number_question), '')
    question.type = type_question
    question.text = request.POST.get('questionName-{}'.format(number_question), '')
    settings = Settings()
    if type_question.lower() == 'range':
        settings.min = request.POST.get('min-{}'.format(number_question), '')
        settings.max = request.POST.get('max-{}'.format(number_question), '')
        settings.step = request.POST.get('step-{}'.format(number_question), '')
    settings.save()
    question.settings = settings
    question.save()
    return question


def create_answers_choices(request, question, number_question):
    count_answer_choice = int(request.POST.get('countOption-{}'.format(number_question), ''))
    settings = question.settings
    for j in range(1, count_answer_choice + 1):
        answer_choice = request.POST.get('option-{}-{}'.format(number_question, j), '')
        answer = AnswerChoice()
        answer.value = answer_choice
        answer.save()
        settings.answer_choice.add(answer)


def create_answer(question, poll):
    new_answer = Answers()
    new_answer.question = question
    new_answer.poll = poll
    new_answer.sum_answer = 0
    new_answer.count_answers = 0
    new_answer.save()
    for i in question.settings.answer_choice.all():
        new_answer.choices.add(i)
    new_answer.save()
