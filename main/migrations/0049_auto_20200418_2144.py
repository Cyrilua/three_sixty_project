# Generated by Django 3.0.4 on 2020-04-18 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_notifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='redirect',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterModelTable(
            name='notifications',
            table='Notifications',
        ),
    ]
