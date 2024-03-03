from django.contrib.auth import get_user_model
from django.db.models import signals
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from lms.models import Course, Subscription


class TestsCRUDSubscription(TestCase):

    def setUp(self):
        signals.post_save.disconnect(sender=Course, dispatch_uid='Course_post_save')
        signals.pre_delete.disconnect(sender=Course, dispatch_uid='Course_pre_delete')

        self.user = get_user_model().objects.create(email='1@1.ru', password='1234')
        self.user.save()

        self.user2 = get_user_model().objects.create(email='2@2.ru', password='1234')
        self.user2.save()

        self.course = Course.objects.create(title='Test Course 1', description='Test Description', owner=self.user)
        self.course2 = Course.objects.create(title='Test Course 2', description='Test Description', owner=self.user)
        self.course3 = Course.objects.create(title='Test Course 3', description='Test Description', owner=self.user)
        self.course4 = Course.objects.create(title='Test Course 4', description='Test Description', owner=self.user2)

        self.client.force_login(self.user)
        url = reverse('lms:sub-create-delete', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)

        self.client.force_login(self.user2)
        url = reverse('lms:sub-create-delete', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 2)

    def test_list(self):
        url = reverse('lms:sub-detail')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'],
            [
                {
                    'id': 10,
                    'user': self.user.id,
                    'course': self.course.id
                },
            ]
        )

    def test_delete_ok(self):
        url = reverse('lms:sub-create-delete', args=[self.course.id])
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(Subscription.objects.filter(user=self.user).count(), 0)
        self.assertEqual(response.data, {'detail': 'Курс Test Course 1 удален из подписок'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_bad(self):
        course_id = 30
        url = reverse('lms:sub-create-delete', args=[course_id])
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(Subscription.objects.filter(user=self.user).count(), 1)
        self.assertEqual(response.data, {'detail': f'Курс с id-{course_id} не найден'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_ok(self):
        self.client.force_login(self.user)
        url = reverse('lms:sub-create-delete', args=[self.course2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 3)
        self.assertEqual(response.data['detail'], f'Курс {self.course2.title} сохранен в подписки')

    def test_create_bad(self):
        course_id = 30
        self.client.force_login(self.user)
        url = reverse('lms:sub-create-delete', args=[course_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Subscription.objects.count(), 2)
        self.assertEqual(response.data['detail'], f'Курс с id-{course_id} не найден')



