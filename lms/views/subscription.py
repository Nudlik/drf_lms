from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework import views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from lms.models import Subscription, Course
from lms.pagination import LMSPagination
from lms.selializers.subscription import SubscriptionSerializer
from lms.yasg import subscription_get, subscription_post, subscription_delete


class SubscriptionDetailAPIView(views.APIView, LMSPagination):

    def get(self, *args, **kwargs):
        subs = Subscription.objects.filter(user=self.request.user)
        page = self.paginate_queryset(subs, self.request)
        serializer = SubscriptionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SubscriptionCreateDeleteAPIView(views.APIView, LMSPagination):

    def post(self, *args, **kwargs):
        course = self.get_course_or_404(Course, course_id=kwargs.get('pk'))
        subs, _ = Subscription.objects.get_or_create(user=self.request.user, course=course)
        serializer = SubscriptionSerializer(subs)
        response = {
            'results': serializer.data,
            'detail': f'Курс {course.title} сохранен в подписки'
        }
        return Response(response, status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        course = self.get_course_or_404(Course, course_id=kwargs.get('pk'))
        Subscription.objects.filter(user=self.request.user, course=course).delete()
        response = {
            'detail': f'Курс {course.title} удален из подписок',
        }
        return Response(response, status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_course_or_404(course, course_id):
        try:
            return get_object_or_404(course, id=course_id)
        except (TypeError, ValueError, ValidationError, Http404):
            response = {
                'detail': f'Курс с id-{course_id} не найден'
            }
            raise Http404(response)

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(exc.args[0], status=404)
        return super().handle_exception(exc)


# декораторы для документации
SubscriptionDetailAPIView = \
    method_decorator(name='get', decorator=subscription_get)(SubscriptionDetailAPIView)

SubscriptionCreateDeleteAPIView = \
    method_decorator(name='post', decorator=subscription_post)(SubscriptionCreateDeleteAPIView)

SubscriptionCreateDeleteAPIView = \
    method_decorator(name='delete', decorator=subscription_delete)(SubscriptionCreateDeleteAPIView)
