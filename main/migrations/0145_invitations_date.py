# Generated by Django 3.0.4 on 2020-08-18 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0144_invitations_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitations',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
