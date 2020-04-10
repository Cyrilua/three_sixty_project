from django.contrib import admin
from .models import Profile, EvaluationMessage, Group, Company


admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Group)

# Register your models here.
