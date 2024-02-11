from rest_framework import viewsets

from lms.models import Course
from lms.selializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
