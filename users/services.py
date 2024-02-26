import stripe
from django.conf import settings
from django.urls import reverse


def checkout_session(name, price, description, domain_url):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'rub',
                    'unit_amount': int(price) * 100,
                    'product_data': {
                        'name': name,
                        'description': description,
                    }
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=domain_url + reverse('users:success'),
        cancel_url=domain_url + reverse('users:canceled'),
    )
    return session


def create_webhook():
    stripe.api_key = settings.STRIPE_SECRET_KEY

