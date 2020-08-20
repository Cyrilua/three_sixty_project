from datetime import datetime

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from main.views.auxiliary_general_methods import get_user_profile
from main.models import Poll, TemplatesPoll, SurveyWizard, NeedPassPoll, CreatedPoll, Questions, Answers, Choice
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDictKeyError
import django.core.mail
from ..create_poll_views import start_create, editor, choose_target, choose_respodents
from django.template.loader import render_to_string



