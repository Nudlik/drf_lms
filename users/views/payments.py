import json
import logging

import stripe
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, views, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from lms.models import Course
from users.models import Payments, Prices
from users.pagination import UserPagination
from users.serializers.payments import PaymentSerializer
from users.services import stripe_checkout_session, finish_payment_entry, begin_payment_entry

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    pagination_class = UserPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ['course', 'lesson', 'payment_method']


@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckOutSession(views.APIView):
    """ Создание сессии для оплаты """

    def post(self, *args, **kwargs):
        product_id = self.kwargs['pk']
        try:  # TODO здесь ссылка может протухнуть и не пройти оплата если юзер в 1 раз решил не оплатить
            # TODO можно в модели сделать поле со временем начала операции, нужно узнать сколько живет ссылка у stripe
            is_payed = Payments.objects.filter(user=self.request.user, course_id=product_id).order_by('-date')
            if is_payed.exists():
                if is_payed[0].payed:
                    return Response({'detail': 'Вы уже оплатили этот курс'}, status=status.HTTP_208_ALREADY_REPORTED)
                else:
                    return Response({'buy_link': is_payed[0].url})

            domain_url = '/'.join(self.request.build_absolute_uri().rsplit('/')[:3])
            product = Course.objects.get(id=product_id)

            stripe_price_id = Prices.objects.get(
                content_type=ContentType.objects.get_for_model(product),
                object_id=product.id
            ).stripe_price_id
            session = stripe_checkout_session(stripe_price_id, domain_url)

            logger.debug(json.dumps(session, indent=4, ensure_ascii=False))
            begin_payment_entry(session, product, self.request.user)

            return Response({'buy_link': session.url})
        except (Course.DoesNotExist, Course.MultipleObjectsReturned):
            return Response({'detail': f'Курс c id {product_id} не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                data={'detail': 'что-то пошло не так при создании сеанса stripe', 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(['GET'])
def success(request):
    """ Успешная оплата """

    logger.info('Успешная оплата')
    return Response({'success': True})


@api_view(['GET'])
def canceled(request):
    """ Отмена оплаты """

    logger.info('Отмена оплаты')
    return Response({'canceled': True})


@api_view(['POST'])
@permission_classes([AllowAny])
def webhook(request):
    """ Обработка событий stripe """

    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        logger.error(e)
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(e)
        return Response(status=400)

    # Handle the event
    logger.debug('Unhandled event type {}'.format(event['type']))
    if event['type'] == 'checkout.session.completed':
        finish_payment_entry(event)

    return Response({'success': True})
