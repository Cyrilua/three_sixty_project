# Generated by Django 3.0.4 on 2020-05-03 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0069_auto_20200503_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
