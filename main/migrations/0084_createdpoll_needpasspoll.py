# Generated by Django 3.0.4 on 2020-05-16 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0083_auto_20200516_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='NeedPassPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Poll')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Profile')),
            ],
            options={
                'db_table': 'NeedPassPolls',
            },
        ),
        migrations.CreateModel(
            name='CreatedPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Poll')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Profile')),
            ],
            options={
                'db_table': 'Created polls',
            },
        ),
    ]
