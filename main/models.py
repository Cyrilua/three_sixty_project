from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    organization = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    objects = models.Manager()

    class Meta:
        db_table = "Profile"

    def __str__(self):
        return 'Profile for user {} {}'.format(self.name, self.surname)


class Company(models.Model):
    name = models.CharField(max_length=20)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    workers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')


class Platform(models.Model):
    name = models.CharField(max_length=50)
    workers = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Position(models.Model):
    name = models.CharField(max_length=20)
    workers = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Command(models.Model):
    name = models.CharField(max_length=20)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    workers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')


class UserCommand(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    commands = models.ForeignKey(Command, on_delete=models.CASCADE)


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


class Group (models.Model):
    def __init__(self, upper_circe, lower_circle):
        self.upper_group = Group
        self.lower_group = Group


# Create your models here.
