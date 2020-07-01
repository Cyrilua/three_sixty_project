import uuid

from main.models import Questions, Poll, Answers, CompanyHR, AnswerChoice, Settings, TextAnswer, TemplatesPoll, Group, \
    NeedPassPoll, CreatedPoll
from main.views.auxiliary_general_methods import *
from main.views.notifications_views import add_notification


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


    #if not user_is_respondent(request, poll):
        #return redirect('/')

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
                change_answer.count_answers += 1
            elif question.type == 'range':
                user_answer = int(request.POST.get('answer-{}'.format(question.id)))
                change_answer.sum_answer += user_answer
                change_answer.count_answers += 1
            else:
                user_answer = request.POST.get('answer-{}'.format(question.id))
                new_text_answer = TextAnswer()
                new_text_answer.answer = change_answer
                new_text_answer.text_answer = user_answer
                new_text_answer.save()
                change_answer.count_answers += 1
            change_answer.save()

        # Удаление прошедшего опрос пользователя
        poll.respondents.remove(auth.get_user(request))
        poll.save()

        profile = get_user_profile(request)
        polls = filter(lambda need_pass: need_pass.profile == profile and need_pass.poll == poll,
                                    NeedPassPoll.objects.all())
        for i in polls:
            i.delete()

        return redirect('/walkthrough_polls_view/')

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

    #if poll.questions.all().first().answers.count_answers < 3:
        #return redirect('/')

    question_answer_result = build_result_questions_answers(poll.questions.all())
    args = {
        'title': 'Получение результатов опроса',
        'name_poll': poll.name_poll,
        'results': question_answer_result
    }
    return render(request, 'main/poll/poll_results.html', args)


def build_result_questions_answers(questions):
    results = []
    id_question = 1
    id_answer_short_text = 1
    id_answer_long_text = 1
    for question in questions:
        result_question = {
            'type': question.type,
            'text': question.text,
            'id': id_question
        }
        id_question += 1
        result_answers = []

        answer = question.answers
        if question.type == 'checkbox' or question.type == 'radio':
            all_choices = question.settings.answer_choice.all()
            sum_votes = 0
            for choice in all_choices:
                sum_votes += choice.count
            if sum_votes == 0:
                sum_votes += 1
            for choice in all_choices:
                temp_answer = {
                    'value': {
                        'percent': choice.count * 100 // sum_votes,
                        'quantity': choice.count
                    }
                }
                temp_text = {'preview': choice.value[0:50:1]}
                if len(choice.value) > 50:
                    temp_text['full'] = choice.value
                temp_answer['text'] = temp_text
                result_answers.append(temp_answer)
        elif question.type == 'range':
            settings = question.settings
            averaged = answer.sum_answer // answer.count_answers
            result_answers = {
                'value': {
                    'percent': averaged * 100 // settings.max,
                    'averaged': averaged,
                    'quantity': answer.count_answers
                }
            }
            result_question['min'] = settings.min
            result_question['max'] = settings.max
        elif question.type == 'small_text':
            for text_answer in answer.textanswer_set.all():
                result_answers.append({
                    'id': id_answer_short_text,
                    'text': text_answer.text_answer
                })
                id_answer_short_text += 1
        else:
            for text_answer in answer.textanswer_set.all():
                result_answers.append({
                    'id': id_answer_long_text,
                    'text': text_answer.text_answer
                })
                id_answer_long_text += 1

        results.append({
            'question': result_question,
            'answers': result_answers
        })

    return results


def new_poll(request, poll_id):
    args = {'title': "Создание опроса"}
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        poll = Poll.objects.get(id=poll_id)
    except:
        return redirect('/')

    args['polls'] = build_template(poll_id)

    if request.method == "POST":
        poll = create_new_poll(request, poll)
        numbers_questions = [int(i) for i in request.POST.get('allQuestionNumbers', '').split(',')]
        print(numbers_questions)
        if len(numbers_questions) > 0:
            create_polls_questions(request, poll, numbers_questions)

        if user_is_hr_or_owner(request):
            return redirect('/search_target_poll/{}/'.format(poll_id))
        return redirect('/communications/')

    return render(request, 'main/poll/new_poll.html', args)


def build_template(poll_id):
    result = []
    for template in TemplatesPoll.objects.all():
        result.append({
            'name': template.name_poll,
            'id': template.id,
            'url': '/new_poll_template/{}/{}/'.format(poll_id, template.id)

        })
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


def select_target(request, profile_id, poll_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        poll = Poll.objects.get(id=poll_id)
    except:
        return redirect('/')
    poll.target = Profile.objects.get(id=profile_id)
    poll.save()
    return redirect('/communications/')


def create_new_poll(request, poll):
    result = poll
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
    result.target = get_user_profile(request)
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
    poll.save()


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


def create_poll_from_template(request, poll_id, template_id):
    args = {'title': "Создание опроса из шаблона"}
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        template = TemplatesPoll.objects.get(id=template_id)
        poll = Poll.objects.get(id=poll_id)
    except:
        return redirect('/new_poll/')
    args['poll'] = build_poll(template)
    args['polls'] = build_template(poll_id)

    if request.method == "POST":
        poll = create_new_poll_from_template(request, poll, template)
        if user_is_hr_or_owner(request):
            return redirect('/search_target_poll/{}/'.format(poll_id))

        return redirect('/communications/')

    return render(request, 'main/poll/custom_poll.html', args)


def create_new_poll_from_template(request, poll, template):
    poll.target = get_user_profile(request)
    poll.initiator = auth.get_user(request)
    poll.name_poll = template.name_poll
    poll.description = template.description
    poll.key = uuid.uuid4().__str__()
    poll.save()
    questions = recreate_questions_from_template(template.questions.all(), poll)
    for question in questions:
        poll.questions.add(question)
    poll.save()
    return poll


def recreate_questions_from_template(questions, poll):
    result = []
    for question in questions:
        temp_question = Questions()
        temp_question.text = question.text
        temp_question.type = question.type

        temp_settings = Settings()
        temp_settings.step = question.settings.step
        temp_settings.min = question.settings.min
        temp_settings.max = question.settings.max
        temp_settings.save()

        temp_question.settings = temp_settings
        temp_question.save()

        for choice in question.settings.answer_choice.all():
            temp_choice = AnswerChoice()
            temp_choice.value = choice.value
            temp_choice.save()
            temp_settings.answer_choice.add(temp_choice)
        temp_settings.save()

        temp_answer = Answers()
        temp_answer.poll = poll
        temp_answer.question = temp_question
        temp_answer.save()
        result.append(temp_question)
    return result


def build_poll(template):
    result = {
        'name': template.name_poll,
        'about': template.description
    }
    questions = template.questions.all()
    list_results_questions = []
    id_question = 1
    for question in questions:
        result_question = {
            'id': id_question,
            'type': question.type,
            'name': question.text
        }
        id_question += 1

        settings = question.settings
        result_question['settings'] = {
            'min': settings.min,
            'max': settings.max,
            'step': settings.step
        }
        result_options = []
        id_option = 1
        for choice in settings.answer_choice.all():
            result_options.append({
                'id': id_option,
                'name': choice.value
            })
            id_option += 1
        result_question['options'] = result_options
        result_question['optionCount'] = len(result_options)
        list_results_questions.append(result_question)
    result['questions'] = list_results_questions
    result['questionCount'] = len(list_results_questions)
    result['allQuestionNumbers '] = get_all_question_number(len(list_results_questions))

    return result


def get_all_question_number(count):
    result = ''
    for i in range(1, count + 1):
        result += str(i)
    return result


def respondent_choice_group(request, group_id):
    args = {'title': "Выбор списка опрашиваемых cреди комманды"}
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        group = Group.objects.get(id=group_id)
    except:
        args['error'] = "Данной комманды не существует"
        return render(request, 'main/poll/respondent_choice.html', args)
    add_positions_and_platform_from_group(group, args)
    users = filter(lambda profile: profile != get_user_profile(request), group.profile_set.all())
    args['users'] = build_users(users)

    if request.method == "POST":
        poll = Poll()
        poll.save()

        created_poll_user = CreatedPoll()
        created_poll_user.profile = get_user_profile(request)
        created_poll_user.poll = poll
        created_poll_user.save()

        profiles = [Profile.objects.get(id=i) for i in request.POST.getlist('selectedUsers', '')]
        for profile in profiles:
            poll.respondents.add(profile.user)
            add_notification(profile,
                             "Вас внесли в список для прохождения опроса",
                             'main:answer_the_poll',
                             poll.id)

            need_pass_poll = NeedPassPoll()
            need_pass_poll.poll = poll
            need_pass_poll.profile = profile
            need_pass_poll.save()

        poll.save()
        return redirect('/new_poll/{}/'.format(poll.id))

    return render(request, 'main/poll/respondent_choice.html', args)


def add_positions_and_platform_from_group(group, args):
    platforms = []
    positions = []
    for profile in group.profile_set.all():
        if profile.platform is not None:
            platforms.append(profile.platform.platform)
        if profile.position is not None:
            positions.append(profile.position)
    add_platform_and_positions(platforms, positions, args)


def add_platform_and_positions(platforms, positions, args):
    platform_result = []
    for platform in platforms:
        platform_result.append({
            'id': platform.id,
            'name': platform.name
        })
    args['platforms'] = platform_result
    position_result = []
    for position in positions:
        position_result.append(
            {
                'id': position.id,
                'name': position.name
            }
        )
    args['positions'] = position_result


def build_users(users):
    results_user = []
    for user in users:
        user_temp = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'patronymic': user.patronymic,
        }
        if user.position is None:
            user_temp['positionId'] = -1
        else:
            user_temp['positionId'] = user.position.id

        if user.platform is None:
            user_temp['platformId'] = -1
        else:
            user_temp['platformId'] = user.platform.platform.id
        results_user.append(user_temp)

    return results_user


def respondent_choice_from_company(request):
    args = {'title': "Выбор списка опрашиваемых"}
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    company = profile.company
    if company is not None:
        add_platform_and_positions([i.platform for i in company.platformcompany_set.all()],
                                   [i.position for i in company.positioncompany_set.all()], args)
    else:
        args['error'] = "Пользователь не состоит в компании"
        return render(request, 'main/poll/respondent_choice.html', args)

    users = filter(lambda profile: profile != get_user_profile(request), company.profile_set.all())
    args['users'] = build_users(users)
    if request.method == "POST":
        poll = Poll()
        poll.save()

        created_poll_user = CreatedPoll()
        created_poll_user.profile = get_user_profile(request)
        created_poll_user.poll = poll
        created_poll_user.save()

        profiles = [Profile.objects.get(id=i) for i in request.POST.getlist('selectedUsers', '')]
        print(profiles)
        for profile in profiles:
            print(profile)
            poll.respondents.add(profile.user)
            add_notification(profile,
                             "Вас внесли в список для прохождения опроса",
                             'main:answer_the_poll',
                             poll.id)
            need_pass_poll = NeedPassPoll()
            need_pass_poll.poll = poll
            need_pass_poll.profile = profile
            need_pass_poll.save()
        poll.save()
        return redirect('/new_poll/{}/'.format(poll.id))

    return render(request, 'main/poll/respondent_choice.html', args)


def walkthrough_polls_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {
        'title': "Вопросы для прохождения",
        'polls': build_need_pass_poll(request)
    }
    return render(request, 'main/poll/walkthrough_polls_view.html', args)


def build_need_pass_poll(request):
    result = []
    profile = get_user_profile(request)
    polls = [i.poll for i in NeedPassPoll.objects.filter(profile=profile)]
    for poll in polls:
        result.append({
            'name': poll.name_poll,
            'url': '/answer_poll/{}/'.format(poll.id)
        })
    return result


def results_polls_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    args = {
        'title': 'Просмотр результата опросов',
        'results': build_list_results_polls(request)
    }

    return render(request, 'main/poll/results_polls_view.html', args)


def build_list_results_polls(request):
    result = []
    profile = get_user_profile(request)
    results_polls = CreatedPoll.objects.filter(profile=profile)
    for result_poll in results_polls:
        try:
            print(result_poll)
            result_temp = {
                'name': result_poll.poll.name_poll
            }
            count_answer = result_poll.poll.questions.all().first().answers.count_answers
            print(count_answer)
            print(result_poll.poll.id)
            #if count_answer >= 3:
            result_temp['url'] = '/result_poll/{}/'.format(result_poll.poll.id)
            result.append(result_temp)
        except:
            continue
    return result


from django.http import JsonResponse, HttpResponse
from django.template import Context, loader



def new_poll_view(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    args = {
        'title': "Быстрый доступ к созданию опросов",
        'companys': build_company(request),
        'teams': build_teams(request)
    }

    if request.is_ajax():
        template = loader.render_to_string('main/tets.html', {'el': ['первый', 'второй', 'третий']})
        return JsonResponse({'newHTML': template}, status=200)

    return render(request, 'main/poll/new_poll_view.html', args)


def build_company(request):
    company = get_user_profile(request).company
    result = [{
        'name': company.name,
        'url': '/respondent_choice_c/',
    }]
    return result


def build_teams(request):
    profile = get_user_profile(request)
    result = []
    for group in profile.groups.all():
        result.append({
            'name': group.name,
            'url': '/respondent_choice_t/{}/'.format(group.id),
        })
    return result
