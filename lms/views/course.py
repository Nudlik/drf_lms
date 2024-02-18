from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from lms.models import Course
from lms.selializers.course import CourseSerializer
from users.permissions import CourseOrLessonOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    perms_methods = {
        'create': [IsAuthenticated, ~IsModerator],
        'destroy': [IsAuthenticated, CourseOrLessonOwner | ~IsModerator],
        'update': [IsAuthenticated, IsAdminUser | CourseOrLessonOwner | IsModerator],
        'partial_update': [IsAuthenticated, IsAdminUser | CourseOrLessonOwner | IsModerator],
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]
