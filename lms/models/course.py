from django.contrib.auth import get_user_model
from django.db import models

from utils.const import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    preview = models.ImageField(upload_to='course', **NULLABLE, verbose_name='Фото')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        related_name='course',
        **NULLABLE,
        verbose_name='Владелец'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, **NULLABLE, verbose_name='Цена')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['id']

    def __str__(self):
        return self.title
