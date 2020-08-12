from django.contrib import admin
from .models import Profile, Group, Company, Poll, TemplatesPoll, NeedPassPoll, CreatedPoll, PositionCompany,\
    PlatformCompany, VerificationCode, Notifications, Questions, Settings, AnswerChoice


admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Group)
admin.site.register(TemplatesPoll)
admin.site.register(Poll)
admin.site.register(NeedPassPoll)
admin.site.register(CreatedPoll)
admin.site.register(PositionCompany)
admin.site.register(PlatformCompany)
admin.site.register(VerificationCode)
admin.site.register(Notifications)
admin.site.register(Questions)
admin.site.register(Settings)
admin.site.register(AnswerChoice)

# Register your models here.
