# Generated by Django 3.0.4 on 2020-08-11 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0136_auto_20200810_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Company'),
        ),
    ]
