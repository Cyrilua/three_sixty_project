from django.db import models


class User (models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    #TODO


class EvaluationMessage (models.Model):
    def __init__(self):
        return
    #TODO


class Group (models.Model):
    def __init__(self, upper_circe, lower_circle):
        self.upper_group = Group
        self.lower_group = Group
    #TODO

# Create your models here.
