<<<<<<< HEAD
from django.contrib.auth.models import User
from django.db import models

from TODO import settings
=======
from django.db import models
from django.contrib.auth.models import User, AbstractUser
>>>>>>> f9bd64681f6d662cbe8ab56681e597bccae2ba79


class Task(models.Model):
    description = models.TextField(max_length=200, blank=False)
    scheduled_deadline = models.DateField(auto_now_add=False)
<<<<<<< HEAD
    real_deadline = models.DateField(auto_now_add=True)
    status = [('TODO', 'TODO'),  ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED'), ('CANCELED', 'CANCELED')]
    task_status = models.CharField(max_length=11, choices=status, default='TODO')
=======
    real_deadline = models.DateField(auto_now_add=False)
    status = [('CANCELED', 'CANCELED'), ('COMPLETED', 'COMPLETED'), ('STARTED', 'STARTED')]
    task_status = models.CharField(max_length=9, choices=status, default='STARTED')
>>>>>>> f9bd64681f6d662cbe8ab56681e597bccae2ba79
    file = models.FileField(default=None, blank=True)
    parent_board = models.ForeignKey('Board', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.description


class Board(models.Model):
    title = models.CharField(max_length=30, blank=False)
<<<<<<< HEAD
    user_creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
=======
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
>>>>>>> f9bd64681f6d662cbe8ab56681e597bccae2ba79
    color = models.CharField(max_length=7, blank=False, default='#AAAAAA')

    def __str__(self):
        return self.title


class Tag(models.Model):
    text = models.CharField(max_length=15, blank=False, default=None)
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text
<<<<<<< HEAD

=======
>>>>>>> f9bd64681f6d662cbe8ab56681e597bccae2ba79
