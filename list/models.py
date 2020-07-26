from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Task(models.Model):
    description = models.TextField(max_length=200, blank=False)
    scheduled_deadline = models.DateField(auto_now_add=False)
    real_deadline = models.DateField(auto_now_add=False)
    status = [('CANCELED', 'CANCELED'), ('COMPLETED', 'COMPLETED'), ('STARTED', 'STARTED')]
    task_status = models.CharField(max_length=9, choices=status, default='STARTED')
    file = models.FileField(default=None, blank=True)
    parent_board = models.ForeignKey('Board', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.description


class Board(models.Model):
    title = models.CharField(max_length=30, blank=False)
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    color = models.CharField(max_length=7, blank=False, default='#AAAAAA')

    def __str__(self):
        return self.title


class Tag(models.Model):
    text = models.CharField(max_length=15, blank=False, default=None)
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text
