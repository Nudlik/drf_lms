from django.contrib.auth import get_user_model
from django.db import models

from utils.const import NULLABLE


class Payments(models.Model):

    class PAYMETHOD(models.TextChoices):
        CASH = 'cash', 'наличные'
        CARD = 'card', 'банковская карта'

    user = models.ForeignKey(
        to=get_user_model(),
        **NULLABLE,
        on_delete=models.SET_NULL,
        related_name='payments',
        verbose_name='Пользователь'
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    course = models.ForeignKey(
        to='lms.Course',
        **NULLABLE,
        on_delete=models.SET_NULL,
        related_name='payments',
        verbose_name='Курс'
    )
    lesson = models.ForeignKey(
        to='lms.Lesson',
        **NULLABLE,
        on_delete=models.SET_NULL,
        related_name='payments',
        verbose_name='Урок'
    )
    payment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Сумма платежа'
    )
    payment_method = models.CharField(choices=PAYMETHOD.choices, max_length=30, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['id']

    def __str__(self):
        user = self.user or 'Неизвестный'
        obj = self.course or self.lesson or 'Удалено'
        return f'{user} оплатил {obj}'
