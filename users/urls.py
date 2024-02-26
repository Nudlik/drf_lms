from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import apps
from users.views.payments import PaymentListView, CreateCheckOutSession, success, canceled, webhook
from users.views.user import UserViewSet

app_name = apps.UsersConfig.name
router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),

    path('buy/course/<int:pk>/', CreateCheckOutSession.as_view(), name='checkout_session'),
    path('buy/success/', success, name='success'),
    path('buy/canceled/', canceled, name='canceled'),

    path('webhook/', webhook, name='webhook'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls))
]
