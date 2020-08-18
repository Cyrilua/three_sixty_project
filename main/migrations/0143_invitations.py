# Generated by Django 3.0.4 on 2020-08-18 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0142_auto_20200817_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(0, 'team'), (1, 'company')], default='team', max_length=15)),
                ('invitation_group_id', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'Invitations',
            },
        ),
    ]
