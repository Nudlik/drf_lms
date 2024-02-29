from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from lms.models import Course
from users.models import Prices
from users.services import stripe_create_price, get_or_create_stripe_product


@receiver(post_save, sender=Course)
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


