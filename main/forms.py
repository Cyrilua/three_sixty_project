from django.forms import ModelForm
from .models import Profile, Company, Group, ProfilePhoto, BirthDate
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('fullname',)


class BirthDateForm(ModelForm):
    class Meta:
        model = BirthDate
        fields = ('birthday',)


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


class UserChangeEmailForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)
