from main.views.auxiliary_general_methods import *
from main.models import CreatedPoll, Poll, NeedPassPoll, TemplatesPoll
from django.shortcuts import redirect, render
from django.template.response import SimpleTemplateResponse
from django.http import JsonResponse


def redirect_for_create(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')
    return redirect('/poll/editor/new/')


def polls_view(request) -> render:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    args = {
        'title': "Опросы",
        'data': {
            'templates': _build_templates(profile),
            'new': {
                'polls': NeedPassPoll.objects.filter(profile=profile, is_viewed=False).count()
            },
        },
        'profile': get_header_profile(profile)
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
        'general': [_collect_template(template) for template in TemplatesPoll.objects.filter(is_general=True,
                                                                                             is_deleted=False)],
        'my': [_collect_template(template) for template in TemplatesPoll.objects.filter(is_general=False,
                                                                                        owner=profile,
                                                                                        is_deleted=False)]
    }
    return result


def _collect_template(template: TemplatesPoll) -> dict:
    collected_template = {
        'name': template.name_poll,
        'url': "/poll/editor/template/{}/".format(template.pk),
        'id': template.pk
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
        return _render_page_no_polls(type_polls)

    result = _pre_render_item_polls(polls)
    if count_polls < count_will_loaded_polls - 1:
        return JsonResponse({'newElems': result, 'is_last': True}, status=200)
    return JsonResponse({'newElems': result, 'is_last': False}, status=200)


def _render_page_no_polls(type_polls: str) -> JsonResponse:
    text_choose = {
        'myPolls': "Вы не провели ни одного опроса",
        'polls': "Сейчас нет опросов для прохождения"
    }
    result = SimpleTemplateResponse('main/includes/bad_search.html', {'text': text_choose[type_polls]})
    result = result.rendered_content
    return JsonResponse({'newElems': result, 'is_last': True}, status=200)


def _pre_render_item_polls(rendered_polls: list) -> str:
    args = {
        'data': {
            'polls': []
        }
    }
    for rendered_poll in rendered_polls:
        rendered_poll: NeedPassPoll
        poll = rendered_poll.poll
        if not poll.is_submitted:
            continue
        collected_poll = _build_poll(poll)
        if type(rendered_poll) == NeedPassPoll:
            collected_poll['is_not_viewed'] = not rendered_poll.is_viewed
            collected_poll['url'] = '/poll/compiling_poll/{}/'.format(poll.pk)
            rendered_poll.is_rendered = True
            rendered_poll.save()
        args['data']['polls'].append(collected_poll)

    response = SimpleTemplateResponse('main/includes/item_polls.html', args)
    result = response.rendered_content
    return result


def _build_poll(poll: Poll) -> dict:
    collected_poll = {
        'title': poll.name_poll,
        'answers_count': poll.count_passed,
        'date': build_date(poll.creation_date),
        'url': '/poll/result/{}/'.format(poll.pk),
        'id': poll.pk,
    }
    if poll.color is not None:
        collected_poll['color'] = poll.color
    target = poll.target
    if target is not None:
        collected_poll['target'] = {
            'name': target.name,
            'surname': target.surname,
            'patronymic': target.patronymic
        }
    return collected_poll


def load_notification_new_poll(request) -> JsonResponse:
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    if request.is_ajax():
        profile = get_user_profile(request)
        polls = NeedPassPoll.objects.filter(profile=profile, is_viewed=False)
        count_polls = polls.count()
        rendered_polls = _render_new_not_viewed_polls(polls)
        print(polls)
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
        collected_poll['is_not_viewed'] = not rendered_poll.is_viewed
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
        template = TemplatesPoll.objects.filter(id=template_id)
        template_first = template.first()
        if template_first is None:
            return JsonResponse({}, status=400)

        if template_first.is_general or template_first.owner != profile:
            return JsonResponse({}, status=400)

        template.update(is_deleted=True)
        return JsonResponse({}, status=200)


def mark_as_viewed(request, poll_id) -> JsonResponse:
    if request.is_ajax():

        try:
            poll: Poll = Poll.objects.get(id=poll_id)
            need_pass_poll: NeedPassPoll = NeedPassPoll.objects.get(poll=poll, profile=get_user_profile(request))
        except ObjectDoesNotExist:
            return JsonResponse({}, status=400)

        need_pass_poll.is_viewed = True
        need_pass_poll.save()
        return JsonResponse({}, status=200)
