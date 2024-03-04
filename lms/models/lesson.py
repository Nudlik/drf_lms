from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from utils.const import NULLABLE


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    preview = models.ImageField(upload_to='lesson', **NULLABLE, verbose_name='Фото')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    link_video = models.CharField(max_length=255, **NULLABLE, verbose_name='Ссылка на видео')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lesson', verbose_name='Курс')
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        related_name='lesson',
        **NULLABLE,
        verbose_name='Владелец'
    )
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['id']

    def __str__(self):
        return f'Курс {self.course} | Урок {self.title}'

    def get_absolute_url(self):
        return reverse('lms:lesson-detail', kwargs={'pk': self.pk})
