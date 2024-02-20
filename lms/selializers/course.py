from rest_framework import serializers

from lms.models import Course
from lms.selializers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson.count', read_only=True)
    lesson = LessonSerializer(read_only=True, many=True)
    subscription = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'preview',
            'description',
            'lesson_count',
            'lesson',
            'owner',
            'subscription',
        ]

    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        course.owner = self.context['request'].user
        return course

    def get_subscription(self, obj):
        user = self.context['request'].user
        return obj.subscription.filter(user=user).exists()
