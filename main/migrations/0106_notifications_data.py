# Generated by Django 3.0.4 on 2020-07-20 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0105_remove_notifications_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='data',
            field=models.DateField(null=True),
        ),
    ]
