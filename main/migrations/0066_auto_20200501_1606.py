# Generated by Django 3.0.4 on 2020-05-01 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0065_auto_20200501_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='question',
        ),
        migrations.AddField(
            model_name='questions',
            name='settings',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Settings'),
        ),
    ]
