from django.db import models

from TODO_list import settings #зачем тебе в сущностях зависимость от настроек? 
# Разнеси модели по разным файлам. Делай всегда так, буто у тебя не простая задача с 3 сущностями/эндпоинтами и узким функционалом, а с мыслью что это дело может расшириться до космических размеров.Проектируй.

class Task(models.Model):
    description = models.TextField(max_length=200, blank=False)
    scheduled_deadline = models.DateField(auto_now_add=False)//
    real_deadline = models.DateField(auto_now_add=True)
    status = [('TODO', 'TODO'),  ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED'),
              ('CANCELED', 'CANCELED')] # зачем каждый статус два раза повяторяется? Есть другая реализация, поищи. Да и вообще это не должно быть тут, поищи куда это дело выносится
    task_status = models.CharField(max_length=11, choices=status, default='TODO_list')
    file = models.FileField(default=None, blank=True)
    parent_board = models.ForeignKey('Board', on_delete=models.CASCADE, default=None)#откуда взялись кавычки у 'Board'?

    def __str__(self):
        return self.description


class Board(models.Model):
    title = models.CharField(max_length=30, blank=False)
    user_creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) //settings.AUTH_USER_MODEL #почему так? почему бы не привязать напрямую к User? Где ты вообще такой пример нашел?
    color = models.CharField(max_length=7, blank=False, default='#AAAAAA')# Здесь можно было бы ограничить регулярным выражением под цвета.

    def __str__(self):
        return self.title


class Tag(models.Model):
    text = models.CharField(max_length=15, blank=False, default=None)
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None)# Вот здесь же напрямую к Task привязал

    def __str__(self):
        return self.text
