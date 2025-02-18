# Generated by Django 3.0.4 on 2020-08-30 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0160_templatespoll_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='RangeAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_on_range', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Answers')),
            ],
            options={
                'db_table': 'RangeAnswer',
            },
        ),
    ]
