# Generated by Django 3.0.4 on 2020-08-03 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0132_templatespoll_is_general'),
    ]

    operations = [
        migrations.AddField(
            model_name='templatespoll',
            name='color',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
