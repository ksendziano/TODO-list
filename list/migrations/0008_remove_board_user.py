# Generated by Django 3.0.4 on 2020-07-15 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0007_auto_20200715_0633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='user',
        ),
    ]
