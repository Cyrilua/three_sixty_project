# Generated by Django 3.0.4 on 2020-08-30 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0158_auto_20200829_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='invitation_group_id',
        ),
        migrations.RemoveField(
            model_name='invitation',
            name='type',
        ),
        migrations.AddField(
            model_name='invitation',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Group'),
        ),
    ]
