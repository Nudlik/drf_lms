from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from lms.models import Course
from lms.selializers.course import CourseSerializer
from users.serializers import UserSerializer


class TestsCRUDCourse(TestCase):

    def setUp(self):
        moder_group, _ = Group.objects.get_or_create(name='moderator')
        self.moderator = get_user_model().objects.create(email='1@1.ru', password='1234')
        self.moderator.groups.add(moder_group)
        self.user = get_user_model().objects.create(email='2@2.ru', password='1234')
        self.user.save()
        self.moderator.save()

    def test_create(self):
        data = {'title': 'Test Course', 'description': 'Test Description'}

        self.client.force_login(self.user)
        url = reverse('lms:course-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        course = CourseSerializer(data=response.data)
        course.is_valid(raise_exception=True)
        print(course.data)
        self.assertEqual(course.data['owner'], self.user.id)

        self.client.force_login(self.moderator)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        course2 = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)

        data = {'title': 'New Title'}

        self.client.force_login(self.user)
        url = reverse('lms:course-detail', args=[course.id])
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(id=course.id).title, 'New Title')

        self.client.force_login(self.moderator)
        url = reverse('lms:course-detail', args=[course2.id])
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(id=course2.id).title, 'New Title')

    def test_delete(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        course2 = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)

        self.client.force_login(self.user)
        url = reverse('lms:course-detail', args=[course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 1)

        self.client.force_login(self.moderator)
        url = reverse('lms:course-detail', args=[course2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 1)
