# Generated by Django 3.0.4 on 2020-04-12 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_auto_20200412_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platformcompany',
            old_name='name',
            new_name='platform',
        ),
    ]
