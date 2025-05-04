import os
from django.db import models, transaction
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Transport(models.Model):
    '''Транспорт, которым возможна отправка'''

    brand = models.CharField(
        verbose_name='Марка',
        max_length=150
    )

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорты'

    def __str__(self):
        return self.brand[:50]


class Status(models.Model):
    '''Статус доставки'''

    name = models.CharField(
        verbose_name='Наименование',
        max_length=150
    )
    color = models.CharField(
        'Цвет',
        null=True
    )

    class Meta:
        verbose_name = 'Статус доставки'
        verbose_name_plural = 'Статусы доставки'

    def __str__(self):
        return self.name[:50]


class Service(models.Model):
    '''Услуга'''

    name = models.CharField(
        verbose_name='Наименование'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name[:50]
    

class Packaging(models.Model):
    '''Упаковка'''

    name = models.CharField(
        verbose_name='Наименование',
        max_length=150
    )

    class Meta:
        verbose_name = 'Упаковка'
        verbose_name_plural = 'Упаковки'

    def __str__(self):
        return self.name[:50]
    

class File(models.Model):
    '''Хранение файлов'''

    file = models.FileField(
        upload_to='media/uploads/',
        verbose_name='Файл'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return os.path.basename(self.file.name)

    
class Delivery(models.Model):
    '''Основная модель которая хранит в себе данные доставок'''

    operator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создатель заказа'
    )
    transport = models.ForeignKey(
        Transport,
        on_delete=models.CASCADE,
        verbose_name='Модель транспорта'
    )
    number = models.CharField(
        max_length=50,
        verbose_name='Номер автомобиля'
    )
    departure_time = models.DateTimeField(
        verbose_name='Время отправки'
    )
    delivery_time = models.DateTimeField(
        verbose_name='Время доставки'
    )
    distance = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Дистанция (км)'
    )
    file = models.ManyToManyField(
        File,
        related_name='files',
        blank=True,
        verbose_name='Файл'
    )
    services = models.ManyToManyField(
        Service,
        verbose_name='Услуги'
    )
    packaging = models.ForeignKey(
        Packaging, 
        on_delete=models.CASCADE,
        verbose_name='Упаковка'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        verbose_name='Статус'
    )
    technical_state = models.BooleanField(
        default=True, 
        verbose_name='Техническое состояние'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    comment = models.CharField(
        'Комментарий',
        max_length=5000,
        blank=True
    )
    fio = models.CharField(
        'ФИО',
        max_length=255,
        blank=True
    )

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['operator_id']),
        ]

    def __str__(self):
        return f'Доставка: №{self.id} | Время доставки: {self.delivery_time} | Составил: {self.operator}'
