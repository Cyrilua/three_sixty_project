# Generated by Django 3.0.4 on 2020-04-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_auto_20200429_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='template_type',
        ),
        migrations.CreateModel(
            name='TemplatesPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_type', models.IntegerField(choices=[(0, 'default'), (1, 'company'), (2, 'team')], default=2)),
                ('name_poll', models.CharField(max_length=50)),
                ('questions', models.ManyToManyField(to='main.Questions')),
            ],
            options={
                'db_table': 'Template',
            },
        ),
    ]
