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


def loading_polls(request, count_polls: int) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    if request.is_ajax():
        profile = get_user_profile(request)
        try:
            count_will_loaded_polls = int(request.GET['count'])
        except TypeError:
            return JsonResponse({}, status=400)
        type_polls = request.GET['type']  # polls, myPolls
        sort = request.GET['sort']  # date, name, quantity
        response = _get_render_sorted_polls_or_bad_search(profile, type_polls, sort, count_polls,
                                                          count_will_loaded_polls)
        return response


def _get_render_sorted_polls_or_bad_search(profile: Profile, type_polls: str, sort: str, count_loaded_polls: int,
                                           count_will_loaded_polls: int) -> JsonResponse:
    choose_parameter_ordering = {
        'date': "-poll__creation_date",
        'name': "poll__name_poll",
        'quantity': "-poll__count_passed"
    }

    try:
        parameter_ordering = choose_parameter_ordering[sort]
    except KeyError:
        return JsonResponse({}, status=400)
    if type_polls == 'myPolls':
        polls = CreatedPoll.objects.filter(profile=profile).order_by(parameter_ordering)[
                count_loaded_polls:count_will_loaded_polls + count_loaded_polls]
    elif type_polls == 'polls':
        polls = NeedPassPoll.objects.filter(profile=profile).order_by(parameter_ordering)[
                count_loaded_polls:count_will_loaded_polls + count_loaded_polls]
    else:
        return JsonResponse({}, status=400)

    count_polls = polls.count()
    if count_polls == 0 and count_loaded_polls == 0:
        text_choose = {
            'myPolls': "Вы не провели ни одного опроса",
            'polls': "Сейчас нет опросов для прохождения"
        }
        result = SimpleTemplateResponse('main/includes/bad_search.html', {'text': text_choose[type_polls]})
        result = result.rendered_content
        return JsonResponse({'newElems': result, 'is_last': True}, status=200)

    result = _pre_render_item_polls(polls)
    if count_polls < count_will_loaded_polls - 1:
        return JsonResponse({'newElems': result, 'is_last': True}, status=200)
    return JsonResponse({'newElems': result, 'is_last': False}, status=200)


def _pre_render_item_polls(rendered_polls: list) -> str:
    args = {
        'data': {
            'polls': []
        }
    }
    for rendered_poll in rendered_polls:
        poll = rendered_poll.poll
        collected_poll = _build_poll(poll)
        if type(rendered_poll) == NeedPassPoll:
            collected_poll['is_viewed'] = not rendered_poll.is_viewed
            print(rendered_poll.is_viewed)
            #collected_poll['is_viewed'] = True
        args['data']['polls'].append(collected_poll)

    print(args)
    response = SimpleTemplateResponse('main/includes/item_polls.html', args)
    result = response.rendered_content
    return result


def _build_poll(poll: Poll) -> dict:
    collected_poll = {
        'title': poll.name_poll,
        'answers_count': poll.count_passed,
        'date': _build_date(poll.creation_date),
        'url': '/poll/result/{}/'.format(poll.id),
        'id': poll.id,
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


def load_notification_new_poll(request) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    if request.is_ajax():
        profile = get_user_profile(request)
        polls = NeedPassPoll.objects.filter(profile=profile, is_viewed=False)
        count_polls = polls.count()
        rendered_polls = _render_new_not_viewed_polls(polls)

        if count_polls > 0:
            return JsonResponse({'notifications': count_polls, 'newElems': rendered_polls}, status=200)
        return JsonResponse({}, status=200)


def _render_new_not_viewed_polls(rendered_polls):
    args = {
        'data': {
            'polls': []
        }
    }
    for rendered_poll in rendered_polls.filter(is_rendered=False):
        rendered_poll: NeedPassPoll

        poll = rendered_poll.poll
        collected_poll = _build_poll(poll)
        # TODO
        collected_poll['is_viewed'] = not rendered_poll.is_viewed
        collected_poll['is_new'] = True
        args['data']['polls'].append(collected_poll)
        rendered_poll.is_rendered = True
        rendered_poll.save()
    response = SimpleTemplateResponse('main/includes/item_polls.html', args)
    result = response.rendered_content
    return result


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


def mark_as_viewed(request, poll_id) -> JsonResponse:
    if request.is_ajax():
        try:
            poll: Poll = Poll.objects.get(id=poll_id)
            need_pass_poll: NeedPassPoll = NeedPassPoll.objects.get(poll=poll)
        except ObjectDoesNotExist:
            return JsonResponse({}, status=400)

        if need_pass_poll.profile != get_user_profile(request):
            return JsonResponse({}, status=400)

        need_pass_poll.is_viewed = True
        need_pass_poll.save()
        return JsonResponse({}, status=200)
