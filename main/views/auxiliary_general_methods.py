import hashlib
import random

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from main.models import Profile, VerificationCode
from django.core.mail import send_mail
from django.conf import settings
UserModel = get_user_model()


def get_user_profile(request):
    user = auth.get_user(request)
    return Profile.objects.get(user=user)


def get_photo_height(width, height):
    result = round(177 / (width / height))
    if result > 300:
        result = 300
    return result


def send_email_validate_message(name: str, surname: str, email: str, code: str) -> None:
    mail_subject = 'Код подтверждения'
    message = render_to_string('main/validate_email.html', {
        'profile': {
            'name': name,
            'surname': surname
        },
        'code': code
    })
    #email = EmailMessage(
    #    mail_subject, message, to=[email]
    #)
    #email.send()
    email_from = settings.EMAIL_HOST_USER
    send_mail(mail_subject, message, email_from, [email,])


def check_code(code: str, email: str) -> bool:
    code_md5 = _get_md5_code(code)
    try:
        verification_code = VerificationCode.objects.get(email=email)
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


def create_verification_code(email: str) -> str:
    try:
        verification_code = VerificationCode.objects.get(email=email)
    except ObjectDoesNotExist:
        verification_code = VerificationCode()
        verification_code.email = email
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
