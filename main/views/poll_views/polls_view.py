from datetime import date

from main.views.auxiliary_general_methods import *
from main.models import CreatedPoll, Poll, NeedPassPoll, TemplatesPoll
from django.shortcuts import redirect, render
from django.template.response import SimpleTemplateResponse
from django.http import JsonResponse


def polls_view(request) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    args = {
        'title': "Опросы",
        'data': {
            'polls': _build_my_polls(profile),
            'templates': _build_templates(profile)
        },
    }
    args['data']['quatity'] = {
        'templates': {
            'general': len(args['data']['templates']['general']),
            'my': len(args['data']['templates']['my'])
        }
    }
    return render(request, 'main/poll/polls_view.html', args)


def _build_templates(profile: Profile) -> dict:
    result = {
        'general': [_collect_template(template) for template in TemplatesPoll.objects.filter(is_general=True)],
        'my': [_collect_template(template) for template in TemplatesPoll.objects.filter(is_general=False,
                                                                                        owner=profile)]
    }
    return result


def _collect_template(template: TemplatesPoll) -> dict:
    collected_template = {
        'name': template.name_poll,
        'url': "/poll/editor/template/{}/".format(template.id),
        'id': template.id
    }
    if not template.is_general:
        collected_template['color'] = template.color
    return collected_template


def _build_my_polls(profile: Profile) -> list:
    count_loaded_polls = 9
    created_polls = CreatedPoll.objects.filter(profile=profile).order_by('poll__creation_date')[:count_loaded_polls]
    result_polls = []
    for created_poll in created_polls:
        collected_poll = _build_poll(created_poll.poll)
        result_polls.append(collected_poll)
    return result_polls


def _build_poll(poll: Poll) -> dict:
    collected_poll = {
        'title': poll.name_poll,
        'answers_count': poll.count_passed,
        'date': _build_date(poll.creation_date),
        'url': '/poll/result/{}/'.format(poll.id)
    }
    if poll.color is not None:
        collected_poll['color'] = poll.color
    target = poll.target
    collected_poll['target'] = {
        'name': target.name,
        'surname': target.surname,
        'patronymic': target.patronymic
    }
    _build_date(poll.creation_date)
    return collected_poll


def _build_date(poll_date: date) -> dict:
    months = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря"
    }

    try:
        month = months[poll_date.month]
    except KeyError:
        return None
    result = {
        'day': poll_date.day,
        'month': month,
        'year': poll_date.year
    }
    return result


def loading_polls(request, count_polls: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    if request.is_ajax():
        profile = get_user_profile(request)
        print(request.GET)
        try:
            count_will_loaded_polls = int(request.GET['count'])
        except TypeError:
            return JsonResponse({}, status=400)

        type = request.GET['type']  # polls, myPolls
        try:
            sort = request.GET['sort']  # date, name, quantity
        except KeyError:
            pass
            #polls = CreatedPoll.objects.filter(profile=profile).order_by('poll__creation_date')[count_polls:count_will_loaded_polls]
        else:
            pass
        polls = CreatedPoll.objects.filter(profile=profile).order_by('poll__creation_date')[
                count_polls:count_will_loaded_polls]
        response = _pre_render_item_polls(polls, count_polls, count_will_loaded_polls)
        return JsonResponse({'newElems': response}, status=200)


def _pre_render_item_polls(polls: list, count_loaded_polls, count_will_loaded_polls) -> str:
    args = {
        'data': {
            'polls': []
        }
    }
    for poll in polls[count_loaded_polls:count_will_loaded_polls]:
        collected_poll = _build_poll(poll.poll)
        args['data']['polls'].append(collected_poll)
    response = SimpleTemplateResponse('main/includes/item_polls.html', args)
    result = response.rendered_content
    return result


def _sort_poll_by_type(polls: list, sorting_type) -> list:
    def sort_by_date(poll: Poll):
        return poll.creation_date

    def sort_by_name(poll: Poll):
        return poll.name_poll

    def sort_by_quantity(poll: Poll):
        return poll.count_passed

    choose_type = {
        'date': sort_by_date,
        'name': sort_by_name,
        'quantity': sort_by_quantity
    }
    polls.sort(key=choose_type[sorting_type])
    return polls


def load_notification_new_poll(request) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    if request.is_ajax():
        profile = get_user_profile(request)
        polls = NeedPassPoll.objects.filter(profile=profile, is_viewed=False)
        count_polls = polls.count()
        if count_polls > 0:
            return JsonResponse({'notifications': count_polls})
        return JsonResponse({}, status=200)


def remove_template(request) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    if request.is_ajax():
        try:
            template_id = int(request.POST['id'])
        except ValueError:
            return JsonResponse({}, status=400)
        profile = get_user_profile(request)
        try:
            template: TemplatesPoll = TemplatesPoll.objects.get(id=template_id)
        except ObjectDoesNotExist:
            return JsonResponse({}, status=400)

        if template.is_general or template.owner != profile:
            return JsonResponse({}, status=400)

        template.delete()
        return JsonResponse({}, status=200)
