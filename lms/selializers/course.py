from rest_framework import serializers

from lms.models import Course
from lms.selializers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson.count', read_only=True)
    lesson = LessonSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'preview',
            'description',
            'lesson_count',
            'lesson',
        ]
