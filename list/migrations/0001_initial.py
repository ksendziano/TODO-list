# Generated by Django 3.0.6 on 2020-08-03 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('color', models.CharField(default='#AAAAAA', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=200)),
                ('scheduled_deadline', models.DateField()),
                ('real_deadline', models.DateField(auto_now_add=True)),
                ('task_status', models.CharField(choices=[('TODO_list', 'TODO_list'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED'), ('CANCELED', 'CANCELED')], default='TODO_list', max_length=11)),
                ('file', models.FileField(blank=True, default=None, upload_to='')),
                ('parent_board', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='list.Board')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default=None, max_length=15)),
                ('parent_task', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='list.Task')),
            ],
        ),
    ]
