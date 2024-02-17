from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Payments


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'phone',
            'city',
            'avatar',
            'password',
            'first_name',
            'last_name',
        ]

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        for field in self.get_fields():
            if field == 'password':
                instance.set_password(validated_data['password'])
            else:
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
        return instance
