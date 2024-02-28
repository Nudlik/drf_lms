from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from users.pagination import UserPagination
from users.permissions import EmailOwner
from users.serializers.user import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    pagination_class = UserPagination
    perms_methods = {
        'create': [AllowAny],
        'update': [IsAuthenticated, EmailOwner | IsAdminUser],
        'partial_update': [IsAuthenticated, EmailOwner | IsAdminUser],
        'destroy': [IsAuthenticated, EmailOwner | IsAdminUser],
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]
