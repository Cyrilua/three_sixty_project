from django.forms import ModelForm
from .models import Profile, Company, Group
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

