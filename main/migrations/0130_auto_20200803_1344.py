# Generated by Django 3.0.4 on 2020-08-03 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0129_auto_20200803_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templatespoll',
            name='type',
        ),
        migrations.AddField(
            model_name='templatespoll',
            name='is_general',
            field=models.BooleanField(default=False),
        ),
    ]
