# Generated by Django 3.0.4 on 2020-07-31 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0121_auto_20200730_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='color',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='poll',
            name='creation_date',
            field=models.DateField(null=True),
        ),
        migrations.DeleteModel(
            name='Draft',
        ),
    ]
