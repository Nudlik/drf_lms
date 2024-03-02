from rest_framework import serializers

from lms.models import Lesson
from lms.validators import CheckLinkVideo


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'preview',
            'description',
            'link_video',
            'course',
            'owner',
        ]
        validators = [CheckLinkVideo(field='link_video')]

    def create(self, validated_data):
        lesson = Lesson.objects.create(**validated_data)
        lesson.owner = self.context['request'].user
        return lesson

    def update(self, instance, validated_data):
        for field in self.get_fields():
            if field == 'owner':  # При правке модератором не меняем владельца
                continue
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
        return instance
