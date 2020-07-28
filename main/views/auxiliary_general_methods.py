import random, hashlib

from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

UserModel = get_user_model()

from main.models import Profile, Moderator, SurveyWizard, VerificationCode


def get_user_profile(request):
    user = auth.get_user(request)
    return Profile.objects.get(user=user)


def get_photo_height(width, height):
    result = round(177 / (width / height))
    if result > 300:
        result = 300
    return result


def send_email_validate_message(request, code: str) -> None:
    user = request.user
    profile = get_user_profile(request)
    mail_subject = 'Код подтверждения'
    message = render_to_string('main/validate_email.html', {
        'profile': {
            'name': profile.name,
            'surname': profile.surname
        },
        'code': code
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def check_code(code: str, profile: Profile) -> bool:
    code_md5 = _get_md5_code(code)
    try:
        verification_code = VerificationCode.objects.get(profile=profile)
    except ObjectDoesNotExist:
        return False
    return verification_code.code == code_md5


def _get_md5_code(code: str) -> str:
    if type(code) != str:
        return None
    code_md5 = hashlib.md5()
    code_md5.update(code.encode('utf-8'))
    result = str(code_md5.digest())
    return result


def create_verification_code(profile: Profile) -> str:
    try:
        verification_code = VerificationCode.objects.get(profile=profile)
    except ObjectDoesNotExist:
        verification_code = VerificationCode()
        verification_code.profile = profile
    code = random.randint(10000, 99999)
    code_str = str(code)
    code_md5 = _get_md5_code(code_str)
    verification_code.code = code_md5
    verification_code.save()
    return code_str


def profile_is_owner(request):
    user = auth.get_user(request)
    profile = get_user_profile(request)
    return profile.company.owner.id == user.id
