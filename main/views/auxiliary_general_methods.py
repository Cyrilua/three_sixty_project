from django.contrib import auth
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import get_user_model

UserModel = get_user_model()

from main.models import Profile, Moderator, SurveyWizard


def get_user_profile(request):
    user = auth.get_user(request)
    profile = Profile.objects.get(user=user)
    return profile


def get_photo_height(width, height):
    result = round(177 / (width / height))
    if result > 300:
        result = 300
    return result


def send_email_validate_message(request):
    current_site = get_current_site(request)
    user = auth.get_user(request)
    mail_subject = 'Activate your email.'
    message = render_to_string('main/validate_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        profile = Profile.objects.get(user=user)
        profile.email_is_validate = True
        profile.save()
        return HttpResponse('Thank you for your email confirmation.')
    else:
        return HttpResponse('Activation link is invalid!')


def profile_is_owner(request):
    user = auth.get_user(request)
    profile = get_user_profile(request)
    return profile.company.owner.id == user.id
