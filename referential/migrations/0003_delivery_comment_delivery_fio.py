# Generated by Django 5.2 on 2025-05-04 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referential', '0002_alter_delivery_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='comment',
            field=models.CharField(blank=True, max_length=5000, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='fio',
            field=models.CharField(blank=True, max_length=255, verbose_name='ФИО'),
        ),
    ]
