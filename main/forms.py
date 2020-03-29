from django.forms import ModelForm
from .models import Profile, Company
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'surname', 'patronymic', 'city')


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name',)
