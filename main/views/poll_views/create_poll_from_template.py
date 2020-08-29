from datetime import datetime

from main.models import Poll, TemplatesPoll, SurveyWizard, NeedPassPoll, CreatedPoll, Questions, Answers, Choice
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail
from .create_poll_views import start_create, editor, choose_target, choose_respodents
from ..auxiliary_general_methods import *
from django.conf import settings
from django.template.loader import get_template


def create_poll_from_template(request, template_id) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        template: TemplatesPoll = TemplatesPoll.objects.get(id=template_id)
    except ObjectDoesNotExist:
        return redirect('/')

    if template.owner is not None and template.owner != get_user_profile(request):
        return redirect('/')
    profile = get_user_profile(request)
    args = {
        'title': "Создание опроса из шаблона",
        'poll': start_create.build_poll(template),
        'profile': get_header_profile(profile),
    }
    if SurveyWizard.objects.filter(profile=profile).exists():
        args['is_master'] = 'is_master'

    return render(request, 'main/poll/new_poll_editor.html', args)


def save_template(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        return editor.save_template(request)


def render_step_1_from_step_3(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = choose_respodents.save_information(request)
        if poll is None:
            return JsonResponse({}, status=400)
        args = editor.get_rendered_page(request, poll)
        return JsonResponse(args, status=200)


def render_step_1_from_step_3_not_master(request: WSGIRequest, template_id) -> JsonResponse:
    return render_step_1_from_step_3(request, template_id)


def render_step_1_from_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = choose_target.save_information(request)
        if poll is None:
            return JsonResponse({}, status=400)

        args = editor.get_rendered_page(request, poll)
        return JsonResponse(args, status=200)


def poll_preview(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        return editor.poll_preview(request)


def poll_editor(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        return editor.poll_editor(request)


def cancel_created_poll(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        try:
            poll = Poll.objects.get(id=int(request.POST['pollId']))
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            return JsonResponse({}, status=200)
        else:
            poll.delete()
            return JsonResponse({}, status=200)


def render_category_teams_on_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        return choose_target.render_category_teams_on_step_2(request)


def render_category_participants_on_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        return choose_target.render_category_participants_on_step_2(request)


def search_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        return choose_target.search(request)


def render_step_2_from_step_3(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = choose_respodents.save_information(request)
        if poll is None:
            return JsonResponse({}, status=400)
        args = choose_target.get_rendered_page(request, poll)
        return JsonResponse(args, status=200)


def render_step_2_from_step_1(request: WSGIRequest, template_id: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    if request.is_ajax():
        poll = editor.save_information(request)
        if poll is None:
            return JsonResponse({}, status=400)
        args = choose_target.get_rendered_page(request, poll)
        return JsonResponse(args, status=200)


def render_step_3_from_step_1_not_master(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = editor.save_information(request)
        poll.target = get_user_profile(request)
        if poll is None:
            return JsonResponse({}, status=400)

        args = choose_respodents.get_rendered_page(request, poll)
        return JsonResponse(args, status=200)


def render_step_3_from_step_2(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = choose_target.save_information(request)
        if poll is None:
            return JsonResponse({}, status=400)
        args = choose_respodents.get_rendered_page(request, poll)
        return JsonResponse(args, status=200)


def render_step_3_from_step_1(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        poll = editor.save_information(request)
        if poll is None:
            return JsonResponse({}, status=400)

        args = choose_respodents.get_rendered_page(request, poll)
        return JsonResponse(args, status=200)


def render_category_teams_on_step_3(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        return choose_respodents.render_category_teams_on_step_3(request)


def render_category_participants_on_step_3(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        return choose_respodents.render_category_participants_on_step_3(request)


def search_step_3(request: WSGIRequest, template_id) -> JsonResponse:
    if request.is_ajax():
        return choose_respodents.search_step_3(request)


def send_poll(request: WSGIRequest, template_id: int) -> JsonResponse:
    if request.is_ajax():
        poll = choose_respodents.save_information(request)
        if poll is None:
            return JsonResponse({}, status=400)

        poll.is_submitted = True
        poll.save()
        _create_unique_key(poll)
        _create_answers(poll)

        profile = get_user_profile(request)
        created_poll = CreatedPoll()
        created_poll.poll = poll
        created_poll.profile = profile
        created_poll.save()

        _sending_emails(request, poll)
        return JsonResponse({}, status=200)


def _create_answers(poll: Poll):
    for question in poll.questions.all():
        question: Questions
        answer = Answers()
        answer.question = question
        answer.poll = poll
        answer.save()
        for choice in question.settings.answer_choice.all():
            new_choice = Choice()
            new_choice.answer_choice = choice
            new_choice.count = 0
            new_choice.save()
            answer.choices.add(new_choice)


def _create_unique_key(poll: Poll):
    poll_id_changed = poll.pk % 1000 + 1000
    initiator_id_changed = poll.initiator.id % 1000 + 1000
    target_id_changed = poll.initiator.id % 1000 + 1000
    date = datetime.today()
    date_changed_str = '{}{}{}{}{}{}{}'.format(date.day, date.month,
                                               date.year, date.hour, date.minute, date.second, date.microsecond)
    key = '{}{}{}{}'.format(poll_id_changed, initiator_id_changed, target_id_changed, date_changed_str)
    poll.key = key
    poll.save()


def _sending_emails(request: WSGIRequest, poll: Poll):
    for need_pass in NeedPassPoll.objects.filter(poll=poll):
        need_pass: NeedPassPoll
        email = need_pass.profile.user.email
        mail_subject = 'Новый опрос'
        link = "{}://{}".format(request._get_scheme(), request.get_host()) + \
               '/poll/compiling_poll_link/{}/'.format(poll.key)  # todo check link

        context = {
            'user': {
                'name': poll.target.name,
                'patronymic': poll.target.patronymic
            },
            'url': link
        }
        message = get_template('main/email/email.html').render(context)
        send_mail(mail_subject, 'dddd', settings.EMAIL_HOST_USER, [email], fail_silently=True, html_message=message)
