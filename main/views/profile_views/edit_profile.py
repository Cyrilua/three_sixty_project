import datetime

from main.forms import ProfileForm, PhotoProfileForm, UserChangeEmailForm
from main.models import ProfilePhoto, BirthDate
from main.views.auxiliary_general_methods import *


def upload_profile_photo(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    profile = get_user_profile(request)
    args = {
        'title': "Добавление фотографии пользователя",
        'form': PhotoProfileForm()
    }

    if request.method == "POST":
        user_photo = request.FILES['photo']
        try:
            profile.profilephoto.photo = user_photo
            profile.profilephoto.save()
        except:
            photo_profile = ProfilePhoto()
            photo_profile.photo = user_photo
            photo_profile.profile = profile
            photo_profile.save()
        return redirect('/')
    return render(request, "main/user/old/upload_photo.html", args)


def edit_profile(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/')

    user = auth.get_user(request)
    profile = get_user_profile(request)
    try:
        birth_date = BirthDate.objects.get(profile=profile)
    except:
        birth_date = datetime.datetime.strptime('1900-1-1', '%Y-%m-%d')
    args = {
        'title': "Редактирование профия",
        'profile_form': ProfileForm({
            'name': profile.name,
            'surname': profile.surname,
            'patronymic': profile.patronymic,
            'birthday': birth_date}),
        'email_form': UserChangeEmailForm({'email': user.email}),
        'profile': profile,
        'user': user
    }

    try:
        photo = profile.profilephoto.photo
        args['photo'] = photo
        args['photo_height'] = get_photo_height(photo.width, photo.height)
    except:
        args['photo'] = None

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile.name = request.POST.get('name', '')
            profile.patronymic = request.POST.get('patronymic', '')
            profile.surname = request.POST.get('surname', '')
            profile.city = request.POST.get('city', '')
            profile.save()
        email_form = UserChangeEmailForm(request.POST)
        if email_form.is_valid():
            new_email = request.POST.get('email', '')
            user.email = new_email
            user.save()
        return redirect('/edit/')
    return render(request, 'main/user/edit.html', args)
