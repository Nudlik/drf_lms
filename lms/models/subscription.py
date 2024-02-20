from django.contrib.auth import get_user_model
from django.db import models

from lms.models import Course
from utils.const import NULLABLE


class Subscription(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='subscription',
        **NULLABLE,
        verbose_name='Владелец'
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name='subscription',
        **NULLABLE,
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['id']

    def __str__(self):
        user = self.user or 'Неизвестный'
        course = self.course or 'Удалено'
        return f'{user} подписался на {course}'
