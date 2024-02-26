from django.contrib.auth import get_user_model
from django.db import models

from utils.const import NULLABLE


class Payments(models.Model):
    class PAYMETHOD(models.TextChoices):
        CASH = 'cash', 'наличные'
        CARD = 'card', 'банковская карта'
        BANCONTACT = 'bancontact'
        EPS = 'eps', 'эквайринг'
        GIROPAY = 'giropay', 'giropay'
        IDEAL = 'ideal', 'ideal'
        P24 = 'p24', 'p24'
        SEPA_DEBIT = 'sepa_debit', 'sepa debit'

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
        **NULLABLE,
        verbose_name='Сумма платежа'
    )
    payment_method = models.CharField(
        choices=PAYMETHOD.choices,
        max_length=30,
        **NULLABLE,
        verbose_name='Способ оплаты'
    )
    session_id = models.CharField(max_length=255, verbose_name='ID сессии')
    payed = models.BooleanField(default=False, verbose_name='Оплачено')
    url = models.URLField(max_length=500, **NULLABLE, verbose_name='Ссылка на оплату')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['id']

    def __str__(self):
        user = self.user or 'Неизвестный'
        obj = self.course or self.lesson or 'Удалено'
        return f'{user} оплатил {obj}'
