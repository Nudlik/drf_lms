from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    del_fields = ['password', 'last_name']

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request.user.is_staff or request.user.is_superuser:
            return data
        elif request.user.id != data.get('id'):
            [data.pop(i) for i in self.del_fields]
        return data
