from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from users.models import Payments
from users.permissions import EmailOwner
from users.serializers import PaymentSerializer, UserSerializer
from utils.pagination import DefaultPagination


class PaymentListView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ['course', 'lesson', 'payment_method']


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    pagination_class = DefaultPagination
    perms_methods = {
        'create': [AllowAny],
        'update': [IsAuthenticated, EmailOwner | IsAdminUser],
        'partial_update': [IsAuthenticated, EmailOwner | IsAdminUser],
        'destroy': [IsAuthenticated, EmailOwner | IsAdminUser],
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]
