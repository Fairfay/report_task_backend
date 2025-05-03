from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    '''Кастомная модель пользователя'''

    patronymic = models.CharField(
        blank=True,
        verbose_name='Отчество',
        max_length=150
    )

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
