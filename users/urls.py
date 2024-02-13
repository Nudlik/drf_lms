from django.urls import path

from users import apps
from users.views import PaymentListView

app_name = apps.UsersConfig.name

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),
]
