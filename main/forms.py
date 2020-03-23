from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'surname', 'patronymic', 'organization', 'position', 'city')

