from rest_framework import serializers

from lms.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'course',
        ]
