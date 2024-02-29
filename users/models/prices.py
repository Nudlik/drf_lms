from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from utils.const import NULLABLE


class Prices(models.Model):

    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    price = models.DecimalField(max_digits=10, decimal_places=2, **NULLABLE, verbose_name='Цена')
    stripe_price_id = models.CharField(max_length=255, verbose_name='id цены в stripe')

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        ordering = ['id']

    def __str__(self):
        return self.product.title
