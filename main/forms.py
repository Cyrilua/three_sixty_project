from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'surname', 'patronymic', 'organization', 'position', 'city')

        def to_lower_username(self):
            self.model.user.username.lower()
