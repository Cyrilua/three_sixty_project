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


class SocialCircle (models.Model):
    def __init__(self, upper_circe, lower_circle):
        self.upper_circe = SocialCircle
        self.lower_circle = SocialCircle
    #TODO

# Create your models here.
