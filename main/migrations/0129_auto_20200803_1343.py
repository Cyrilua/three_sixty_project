# Generated by Django 3.0.4 on 2020-08-03 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0128_auto_20200803_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='poll',
        ),
        migrations.AddField(
            model_name='poll',
            name='questions',
            field=models.ManyToManyField(to='main.Questions'),
        ),
    ]
