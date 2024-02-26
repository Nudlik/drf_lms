import json
import logging

import stripe
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, views, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from lms.models import Course
from users.models import Payments
from users.serializers.payments import PaymentSerializer
from users.services import checkout_session
from utils.pagination import DefaultPagination

logger = logging.getLogger(__name__)


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ['course', 'lesson', 'payment_method']


@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckOutSession(views.APIView):

    def post(self, *args, **kwargs):
        product_id = self.kwargs['pk']
        domain_url = '/'.join(self.request.build_absolute_uri().rsplit('/')[:3])
        try:
            is_payed = Payments.objects.filter(user_id=self.request.user.id, course_id=product_id).order_by('-date')
            if is_payed.exists():
                if is_payed[0].payed:
                    return Response({'detail': 'Вы уже оплатили этот курс'}, status=status.HTTP_208_ALREADY_REPORTED)
                else:
                    return Response({'buy_link': is_payed[0].url})

            product = Course.objects.get(id=product_id)
            session = checkout_session(
                name=product.title,
                price=product.price,
                description=product.description,
                domain_url=domain_url,
            )
            logger.debug(json.dumps(session, indent=4, ensure_ascii=False))
            payment = Payments.objects.create(
                session_id=session.id,
                url=session.url,
                user=self.request.user,
                course=product
            )
            payment.save()
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
    logger.info('Успешная оплата')
    return Response({'success': True})


@api_view(['GET'])
def canceled(request):
    return Response({'canceled': True})


@api_view(['POST'])
@permission_classes([AllowAny])
def webhook(request):
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

    return Response({'success': True})
