from django.contrib import auth

from main.models import Profile


def get_user_profile(request):
    user = auth.get_user(request)
    return Profile.objects.get(user=user)


def get_photo_height(width, height):
    result = round(177 / (width / height))
    if result > 300:
        result = 300
    return result
