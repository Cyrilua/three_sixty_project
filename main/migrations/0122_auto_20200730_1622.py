# Generated by Django 3.0.8 on 2020-07-30 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0121_merge_20200730_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default='', max_length=100),
        ),
    ]
