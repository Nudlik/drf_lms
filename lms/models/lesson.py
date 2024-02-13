from django.db import models

from utils.const import NULLABLE


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    preview = models.ImageField(upload_to='lesson', **NULLABLE, verbose_name='Фото')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    link_video = models.CharField(max_length=255, **NULLABLE, verbose_name='Ссылка на видео')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lesson', verbose_name='Курс')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['id']

    def __str__(self):
        return self.title
