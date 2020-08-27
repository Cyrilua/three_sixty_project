import hashlib
import random
from datetime import date

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from main.models import Profile, VerificationCode, PositionCompany, PlatformCompany, Company
from django.db.models import Q

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
    email = EmailMessage(
        mail_subject, message, to=[email]
    )
    email.send()


def check_code(code: str, email: str) -> bool:
    code_md5 = _get_md5_code(code)
    try:
        verification_code = VerificationCode.objects.get(email=email)
    except ObjectDoesNotExist:
        return False
    return verification_code.code == code_md5


def _get_md5_code(code: str) -> str:
    if type(code) != str:
        code = str(code)
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


def build_date(input_date: date) -> dict:
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
        month = months[input_date.month]
    except KeyError:
        return {'day': input_date.day,
        'month': input_date.month,
        'year': input_date.year}
    result = {
        'day': input_date.day,
        'month': month,
        'year': input_date.year
    }
    return result


def get_header_profile(profile: Profile) -> dict:
    args = {
        'name': profile.name,
        'surname': profile.surname,
    }
    company = profile.company
    if company is not None:
        args['company'] = {
            'id': company.pk,
            'name': company.name,
        }
    return args


def get_search_result_for_profiles(profiles, user_input: list, company: Company):
    for input_iter in user_input:
        profiles = profiles.filter(
            Q(name__istartswith=input_iter) |
            Q(surname__istartswith=input_iter) |
            Q(patronymic__istartswith=input_iter))
        if company is not None:
            id_profiles_by_positions = PositionCompany.objects \
                .filter(company=company) \
                .filter(name__istartswith=input_iter) \
                .values_list('profile__id', flat=True)
            profiles_by_positions = Profile.objects.filter(id__in=id_profiles_by_positions)
            id_profiles_by_platforms = PlatformCompany.objects \
                .filter(company=company) \
                .filter(name__istartswith=input_iter) \
                .values_list('profile__id', flat=True)
            profiles_by_platforms = Profile.objects.filter(id__in=id_profiles_by_platforms)
            profiles = profiles.union(profiles_by_platforms, profiles_by_positions)
    return profiles
