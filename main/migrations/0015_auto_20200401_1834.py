# Generated by Django 3.0.4 on 2020-04-01 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200401_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='command',
            name='workers',
        ),
        migrations.DeleteModel(
            name='UserCommand',
        ),
    ]
