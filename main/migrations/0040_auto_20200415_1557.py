# Generated by Django 3.0.4 on 2020-04-15 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_auto_20200415_1519'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='answers',
            table='Answer',
        ),
        migrations.AlterModelTable(
            name='questions',
            table='Questions',
        ),
    ]
