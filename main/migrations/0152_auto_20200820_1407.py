# Generated by Django 3.0.4 on 2020-08-20 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0151_auto_20200820_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='count_profile_answers',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelTable(
            name='answerchoice',
            table='AnswerChoice',
        ),
    ]
