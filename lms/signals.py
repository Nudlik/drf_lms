from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from lms.models import Course
from users.models import Prices
from users.services import stripe_create_price, get_or_create_stripe_product, stripe_delete_product


@receiver(post_save, sender=Course, dispatch_uid='Course_post_save')
def post_save_stripe_price_id(sender, instance, created, **kwargs):
    get_or_create_stripe_product(instance)

    prices, _ = Prices.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id
    )

    if created or instance.price != prices.price:
        prices.price = instance.price
        prices.stripe_price_id = stripe_create_price(instance).id

    prices.save()


@receiver(pre_delete, sender=Course, dispatch_uid='Course_pre_delete')
def pre_delete_course(sender, instance, **kwargs):
    stripe_delete_product(instance)

    prices = Prices.objects.get(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id
    )
    prices.delete()
