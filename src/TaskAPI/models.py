from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


from datetime import datetime


class Task(models.Model):
    STATUS_CHOICES = (
        ('N','Новая'),
        ('Z','Запланированая'),
        ('V', 'В работе'),
        ('E','Завершенная'),
    )
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    date = models.DateTimeField('Время создания', default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    end_date = models.DateField('Планируемая дата завершения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Action(models.Model):
    text = models.CharField('Описание действия',max_length=200)
    date = models.DateTimeField('Время создания', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.text

        

