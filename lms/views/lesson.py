from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from lms.models import Lesson
from lms.selializers.lesson import LessonSerializer
from users.permissions import IsModerator, CourseOrLessonOwner, IsModeratorObj


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | CourseOrLessonOwner | IsModerator]


class LessonDeleteView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, CourseOrLessonOwner | ~IsModeratorObj]
