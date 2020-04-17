import re

from django.shortcuts import redirect
from django.shortcuts import render

from main.models import Questions
from main.views.auxiliary_general_methods import *


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
            # TODO Перенаправлять на нужную страницу
            return redirect('/')
        else:
            args['title'] = "Вопрос уже существует"
            return render(request, 'main/new_question.html', args)
    return render(request, 'main/new_question.html', args)
