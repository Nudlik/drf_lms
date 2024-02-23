from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from users.models import Payments
from users.serializers.payments import PaymentSerializer
from utils.pagination import DefaultPagination


class PaymentListView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ['course', 'lesson', 'payment_method']
