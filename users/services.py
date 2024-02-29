import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.urls import reverse

from users.models import Payments

stripe.api_key = settings.STRIPE_SECRET_KEY
WEB_HOOK_DESCRIPTION = 'checkout.session.completed'


def stripe_checkout_session(
        stripe_price_id: str,
        domain_url: str
) -> stripe.checkout.Session:
    """ Создание сеанса stripe """

    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': stripe_price_id,
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=domain_url + reverse('users:success'),
        cancel_url=domain_url + reverse('users:canceled'),
    )
    return session


def create_webhook() -> dict:
    """ Создание webhook """

    try:
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


def get_webhook() -> dict | None:
    """ Получение webhook """

    try:
        web_hooks: dict = stripe.WebhookEndpoint.list()
        for web_hook in web_hooks['data']:
            if web_hook.get('description') == WEB_HOOK_DESCRIPTION:
                return web_hook
        return None
    except Exception as e:
        print(f'Ошибка при получении webhook {e}')


def stripe_create_product(product: QuerySet.get) -> stripe.Product:
    """ Создание продукта stripe """

    stripe_product = stripe.Product.create(
        name=product.title,
        id=generate_id(product),
        description=product.description,
    )
    return stripe_product


def stripe_create_price(product: QuerySet.get) -> stripe.Price:
    """ Создание цены stripe """

    stripe_price = stripe.Price.create(
        currency='rub',
        unit_amount=int(product.price) * 100,
        product=generate_id(product),
    )
    return stripe_price


def begin_payment_entry(
        session: stripe.checkout.Session,
        product: stripe.Product,
        user: get_user_model()
) -> None:
    """ Создание записи о платеже """

    payment = Payments.objects.create(
        session_id=session.id,
        url=session.url,
        user=user,
        course=product
    )
    payment.save()


def get_or_create_stripe_product(product: QuerySet.get) -> stripe.Product:
    """ Получение или создание продукта stripe """

    product_id = generate_id(product)
    try:
        stripe_product = stripe.Product.retrieve(product_id)
    except stripe.error.InvalidRequestError:
        return stripe_create_product(product)
    else:
        return stripe_product


def set_stripe_price(prices: QuerySet.get) -> stripe.Price:
    """ Установка существующей цены stripe """

    stripe_price = stripe.Price.retrieve(prices.stripe_price_id)
    return stripe_price


def stripe_delete_product(product: QuerySet.get) -> stripe.Product:
    """
    Удаление продукта у stripe
    Возвращает удаленный продукт
    На самом деле это имитация удаления, страйп ничего не удаляет :(
    """

    product_id = generate_id(product)
    stripe_product = stripe.Product.modify(id=product_id, active=False)
    return stripe_product


def generate_id(product: QuerySet.get) -> str:
    """ Генерация id продукта для stripe """

    return f'{product.__class__.__name__}_id_{product.id}'


def finish_payment_entry(event: stripe.Event) -> None:
    """ Завершение платежа """

    session = event['data']['object']
    session_id = session['id']
    payment_method = session['payment_method_types'][0] if len(session['payment_method_types']) else 'card'
    payment_amount = session['amount_total'] / 100

    payment = Payments.objects.get(session_id=session_id)
    payment.payed = True
    payment.session_id = session_id
    payment.payment_amount = payment_amount
    payment.payment_method = payment_method
    payment.save()
