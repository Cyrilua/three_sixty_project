# Generated by Django 3.0.4 on 2020-04-01 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20200401_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platforms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='platformcompany',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Platforms'),
        ),
    ]
