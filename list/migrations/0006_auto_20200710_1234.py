# Generated by Django 3.0.4 on 2020-07-10 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0005_auto_20200710_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='real_deadline',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='scheduled_deadline',
            field=models.DateField(auto_now_add=True),
        ),
    ]
