# Generated by Django 3.0.4 on 2020-08-31 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0163_auto_20200831_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Company'),
        ),
        migrations.AddField(
            model_name='poll',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Group'),
        ),
    ]
