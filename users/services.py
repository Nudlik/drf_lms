import stripe
from django.conf import settings
from django.urls import reverse

WEB_HOOK_DESCRIPTION = 'checkout.session.completed'


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
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        web_hook_url = reverse('users:webhook')
        web_hook = get_webhook()
        if web_hook is None:
            web_hook = stripe.WebhookEndpoint.create(
                enabled_events=['checkout.session.completed'],
                url=f'{settings.STRIPE_WEBHOOK_URL}{web_hook_url}',
                description='checkout.session.completed',
            )
        return web_hook
    except Exception as e:
        print(f'Ошибка при создании webhook {e}')


def get_webhook():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        web_hooks = stripe.WebhookEndpoint.list()
        for web_hook in web_hooks['data']:
            if web_hook.get('description') == WEB_HOOK_DESCRIPTION:
                return web_hook
        return None
    except Exception as e:
        print(f'Ошибка при получении webhook {e}')
