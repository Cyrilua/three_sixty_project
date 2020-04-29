from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    platform = models.ForeignKey('PlatformCompany', on_delete=models.CASCADE, null=True)
    position = models.ForeignKey('Position', on_delete=models.CASCADE, null=True)
    groups = models.ManyToManyField('Group', null=True)
    city = models.CharField(max_length=20)
    objects = models.Manager()
    last_poll = models.OneToOneField('Poll', on_delete=models.CASCADE, null=True)
    answers_sum = models.IntegerField(default=0)
    count_answers = models.IntegerField(default=0)

    class Meta:
        db_table = "Profile"

    def __str__(self):
        return 'Profile for user {} {}'.format(self.name, self.surname)


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

    class Meta:
        db_table = "Profile photo"

    def __str__(self):
        return "Profile: {}".format(self.profile)


class Notifications (models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    redirect = models.CharField(max_length=100, default='')
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
    #user = models.ManyToManyField(User)
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
    questions = models.ManyToManyField('Questions')

    class Meta:
        db_table = 'Template'

    def __str__(self):
        return self.name_poll


class Poll(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    name_poll = models.CharField(max_length=50, default='')
    questions = models.ManyToManyField('Questions')
    respondents = models.ManyToManyField(User)
    objects = models.Manager()
    #start_date = models.DateField()
    #end_date = models.DateField()

    class Meta:
        db_table = "Poll"

    def __str__(self):
        return self.name_poll


class Questions(models.Model):
    TYPE_CHOICES = [
        ('text', 0),
        ('radio', 1),
        ('range', 2),
    ]

    type = models.CharField(choices=TYPE_CHOICES, default='range', max_length=10)
    text = models.CharField(max_length=100)
    objects = models.Manager()

    class Meta:
        db_table = "Questions"

    def __str__(self):
        return self.text


class Answers(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE)
    sum_answer = models.IntegerField(default=0)
    count_answers = models.IntegerField(default=0)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    class Meta:
        db_table = "Answer"

    def __str__(self):
        return "{}: {}".format(self.question, self.sum_answer)


class OpenQuestions(models.Model):
    question = models.CharField(max_length=100)
    objects = models.Manager()


class OpenAnswer(models.Model):
    open_question = models.OneToOneField(OpenQuestions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    objects = models.Manager()


class EvaluationMessage (models.Model):
    def __init__(self):
        return
    #TODO


# Create your models here.
