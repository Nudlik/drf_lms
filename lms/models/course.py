from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

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
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    time_last_send = models.DateTimeField(default=timezone.now, verbose_name='Время последнего уведомления')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lms:course-detail', kwargs={'pk': self.pk})
