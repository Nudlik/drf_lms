from rest_framework import serializers

from lms.models import Lesson


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

    def create(self, validated_data):
        lesson = Lesson.objects.create(**validated_data)
        lesson.owner = self.context['request'].user
        return lesson
