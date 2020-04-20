from django.shortcuts import redirect
from django.shortcuts import render

from main.models import Questions, Poll, Answers
from main.views.auxiliary_general_methods import *


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
        answer.answer = answer_user
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
