from rest_framework import serializers

from lms.models import Lesson
from utils.validators import CheckLinkVideo


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
