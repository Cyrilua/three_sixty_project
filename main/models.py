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

    class Meta:
        db_table = "Profile"

    def __str__(self):
        return 'Profile for user {} {}'.format(self.name, self.surname)


class Company(models.Model):
    name = models.CharField(max_length=20)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=36, unique=True, default='')

    class Meta:
        db_table = "Company"

    def __str__(self):
        return 'Company name: {}, Owner: {}'.format(self.name, self.owner)


class PlatformCompany(models.Model):
    name = models.ForeignKey('Platforms', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = "Platforms in company"

    def __str__(self):
        return '{} in company {}'.format(self.name, self.company)


class Platforms (models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "Platforms"

    def __str__(self):
        return self.name


class PositionCompany (models.Model):
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = "Positions in company"


class Position(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "Positions"

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=20, default='')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+', null=True)
    #user = models.ManyToManyField(User)
    key = models.CharField(max_length=36, default='')

    class Meta:
        db_table = "Groups"

    def __str__(self):
        return "Group \"{}\" with owner \"{}\"".format(self.name, self.owner)


class Poll(models.Model):
    assessed = models.OneToOneField(User, on_delete=models.CASCADE)
    respondent = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')
    start_date = models.DateField()
    end_date = models.DateField()


class Questions(models.Model):
    question = models.CharField(max_length=100)


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)


class OpenQuestions(models.Model):
    question = models.CharField(max_length=100)


class OpenAnswer(models.Model):
    open_question = models.OneToOneField(OpenQuestions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)


class EvaluationMessage (models.Model):
    def __init__(self):
        return
    #TODO


# Create your models here.
