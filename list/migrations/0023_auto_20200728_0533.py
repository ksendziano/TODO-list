# Generated by Django 3.0.4 on 2020-07-28 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0022_auto_20200728_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='real_deadline',
            field=models.DateField(blank=True, default=None),
        ),
    ]
