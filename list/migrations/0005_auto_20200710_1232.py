# Generated by Django 3.0.4 on 2020-07-10 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0004_auto_20200710_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='real_deadline',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='scheduled_deadline',
            field=models.DateField(),
        ),
    ]
