from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from lms.apps import LmsConfig
from lms.models import Course
from lms.pagination import LMSPagination
from lms.selializers.course import CourseSerializer
from lms.tasks import task_send_mail_for_subscribers, get_absolute_url
from users.permissions import CourseOrLessonOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LMSPagination
    perms_methods = {
        'create': [IsAuthenticated, ~IsModerator],
        'destroy': [IsAuthenticated, CourseOrLessonOwner, ~IsModerator],
        'update': [IsAuthenticated, IsAdminUser | CourseOrLessonOwner | IsModerator],
        'partial_update': [IsAuthenticated, IsAdminUser | CourseOrLessonOwner | IsModerator],
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):
        instance = serializer.instance

        # проверка на то, что уведомление отправляется только в том случае, если курс не обновлялся более четырех часов.
        instance.time_update = timezone.now()
        if instance.time_update > instance.time_last_send + LmsConfig.TIME_COOLDOWN:
            instance.time_last_send = timezone.now()

            subscribers = instance.subscription.all()
            for subscriber in subscribers:
                url = get_absolute_url(self.request, instance)

                task_send_mail_for_subscribers.delay(
                    subject=f'В курс "{instance.title}" добавился новый контент',
                    message=f'Перейдите по ссылке для просмотра {url}',
                    email=subscriber.user.email,
                )

        super().perform_update(serializer)
