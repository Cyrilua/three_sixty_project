from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, default='')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    platform = models.ForeignKey('PlatformCompany', on_delete=models.CASCADE, null=True)
    position = models.ForeignKey('Position', on_delete=models.CASCADE, null=True)
    groups = models.ManyToManyField('Group', null=True)
    objects = models.Manager()

    class Meta:
        db_table = "Profile"

    def __str__(self):
        return 'Profile for user {}'.format(self.fullname)


class BirthDate(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    birthday = models.DateField()

    class Meta:
        db_table = 'BirthDate'


class CreatedPoll(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    poll = models.OneToOneField('Poll', on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = "Created polls"


class NeedPassPoll(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = "NeedPassPolls"


class CompanyAdmins(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    class Meta:
        db_table = 'Admins'

    def __str__(self):
        return '{} in company \"{}\"'.format(self.profile, self.company)


class CompanyHR(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    class Meta:
        db_table = 'HR'

    def __str__(self):
        return '{} in company \"{}\"'.format(self.profile, self.company)


class ProfilePhoto (models.Model):
    photo = models.ImageField(null=True, upload_to='media/images/', blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = "Profile photo"

    def __str__(self):
        return "Profile: {}".format(self.profile)


class Notifications (models.Model):
    name = models.CharField(max_length=50, default='')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    redirect = models.CharField(max_length=100, default='')
    key = models.CharField(max_length=36, null=True)
    objects = models.Manager()

    class Meta:
        db_table = "Notifications"

    def __str__(self):
        return self.redirect


class Company(models.Model):
    name = models.CharField(max_length=20)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=36, unique=True, default='')
    objects = models.Manager()

    class Meta:
        db_table = "Company"

    def __str__(self):
        return 'Company name: {}, Owner: {}'.format(self.name, self.owner)


class PlatformCompany(models.Model):
    platform = models.ForeignKey('Platforms', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = "Platforms in company"

    def __str__(self):
        return '{}'.format(self.platform)


class Platforms (models.Model):
    name = models.CharField(max_length=50, unique=True)
    objects = models.Manager()

    class Meta:
        db_table = "Platforms"

    def __str__(self):
        return self.name


class PositionCompany (models.Model):
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = "Positions in company"

    def __str__(self):
        return '{}'.format(self.position)


class Position(models.Model):
    name = models.CharField(max_length=20, unique=True)
    objects = models.Manager()

    class Meta:
        db_table = "Positions"

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=20, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    key = models.CharField(max_length=36, default='')
    objects = models.Manager()

    class Meta:
        db_table = "Groups"

    def __str__(self):
        return "Group \"{}\" with owner \"{}\"".format(self.name, self.owner)


class TemplatesPoll(models.Model):
    TYPE_CHOICES = [
        ('default', 0),
        ('company', 1),
        ('team', 2)
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='default')
    name_poll = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True)
    questions = models.ManyToManyField('Questions')
    objects = models.Manager()

    class Meta:
        db_table = 'Template'

    def __str__(self):
        return self.name_poll


class Draft(models.Model):
    poll = models.ManyToManyField('Poll')
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = 'Draft'


class Poll(models.Model):
    key = models.CharField(max_length=36, default='')
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    target = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name_poll = models.CharField(max_length=50, default='')
    respondents = models.ManyToManyField(User)
    description = models.CharField(max_length=500, null=True)
    objects = models.Manager()
    #start_date = models.DateField()
    #end_date = models.DateField()

    class Meta:
        db_table = "Poll"

    def __str__(self):
        return self.name_poll


class Questions(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    settings = models.OneToOneField('Settings', on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=100)
    objects = models.Manager()

    class Meta:
        db_table = "Questions"

    def __str__(self):
        return self.text


class Settings(models.Model):
    TYPE_CHOICES = [
        ('small_text', 0),
        ('radio', 1),
        ('range', 2),
        ('checkbox', 3),
    ]

    type = models.CharField(choices=TYPE_CHOICES, default='range', max_length=10)
    min = models.IntegerField(null=True)
    max = models.IntegerField(null=True)
    step = models.IntegerField(null=True)
    answer_choice = models.ManyToManyField('AnswerChoice')
    objects = models.Manager()

    class Meta:
        db_table = "Questions settings"


class AnswerChoice(models.Model):
    text = models.CharField(max_length=50, default='')
    objects = models.Manager()

    class Meta:
        db_table = "Answer choice"

    def __str__(self):
        return self.text


class Answers(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    choices = models.ForeignKey(AnswerChoice, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, null=True)
    range_number = models.IntegerField(null=True)
    objects = models.Manager()

    class Meta:
        db_table = "Answer"
