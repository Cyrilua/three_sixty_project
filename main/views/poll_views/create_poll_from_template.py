from main.views.auxiliary_general_methods import *
from main.models import Poll, TemplatesPoll
from django.shortcuts import redirect, render


def create_poll_from_template(request, template_id):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    try:
        template = TemplatesPoll.objects.get(id = template_id)
    except ObjectDoesNotExist:
        return redirect('/')

    args = {
        ''
    }

    return render(request, 'main/poll/new_poll_editor.html', args)
