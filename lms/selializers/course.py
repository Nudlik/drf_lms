from rest_framework import serializers

from lms.models import Course


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'preview',
            'description',
            'lesson_count',
        ]

    def get_lesson_count(self, obj):
        return obj.lesson.count()
