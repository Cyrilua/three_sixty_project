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
    organization = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    city = models.CharField(max_length=20)

    class Meta:
        db_table = "user"

    def __str__(self):
        return 'Profile for user {} {}'.format(self.name, self.surname)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
