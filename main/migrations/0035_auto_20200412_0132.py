# Generated by Django 3.0.4 on 2020-04-11 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_auto_20200411_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='positioncompany',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Company'),
        ),
    ]
