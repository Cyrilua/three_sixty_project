# Generated by Django 3.0.4 on 2020-07-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0120_remove_profilephoto_photo_hex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default='', max_length=100),
        ),
    ]
