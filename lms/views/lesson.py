from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from lms.apps import LmsConfig
from lms.models import Lesson, Subscription
from lms.pagination import LMSPagination
from lms.selializers.lesson import LessonSerializer
from lms.tasks import get_absolute_url, task_send_mail_for_subscribers
from users.permissions import IsModerator, CourseOrLessonOwner


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LMSPagination


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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        course = instance.course
        if course.time_last_send + LmsConfig.TIME_COOLDOWN < instance.time_update:
            course.time_last_send = timezone.now()
            course.save()

            subscribers = Subscription.objects.filter(course_id=instance.course_id)
            for subscriber in subscribers:
                url = get_absolute_url(request, instance)

                task_send_mail_for_subscribers.delay(
                    subject=f'В курсе "{course.title}" обновился урок {instance.title}',
                    message=f'Перейдите по ссылке для просмотра {url}',
                    email=subscriber.user.email,
                )

        return Response(serializer.data)


class LessonDeleteView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, CourseOrLessonOwner, ~IsModerator]
