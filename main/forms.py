from django.forms import ModelForm
from .models import Profile, Company, Group, ProfilePhoto
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'surname', 'patronymic', 'city')


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name',)


class TeamForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name',)


class PhotoProfileForm(ModelForm):
    class Meta:
        model = ProfilePhoto
        fields = ('photo',)
