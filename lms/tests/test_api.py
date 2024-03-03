from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import signals
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from lms.models import Course, Lesson
from lms.selializers.lesson import LessonSerializer


class TestsCRUDCourse(TestCase):

    def setUp(self):
        signals.post_save.disconnect(sender=Course, dispatch_uid='Course_post_save')
        signals.pre_delete.disconnect(sender=Course, dispatch_uid='Course_pre_delete')

        moder_group, _ = Group.objects.get_or_create(name='moderator')
        self.moderator = get_user_model().objects.create(email='1@1.ru', password='1234')
        self.moderator.groups.add(moder_group)
        self.user = get_user_model().objects.create(email='2@2.ru', password='1234')
        self.user2 = get_user_model().objects.create(email='3@3.ru', password='1234')

        self.user.save()
        self.moderator.save()
        self.user2.save()

    def test_create(self):
        data = {'title': 'Test Course', 'description': 'Test Description'}
        self.client.force_login(self.user)
        url = reverse('lms:course-list')
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)

        # Тут почему то не создается реквест в сериализаторе D:
        # course = CourseSerializer(data=response.data)
        # course.is_valid(raise_exception=True)
        # self.assertEqual(course.data['owner'], self.user.id)

    def test_create_moderator(self):
        data = {'title': 'Test Course', 'description': 'Test Description'}
        self.client.force_login(self.moderator)
        url = reverse('lms:course-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        data = {'title': 'New Title'}
        self.client.force_login(self.user)
        url = reverse('lms:course-detail', args=[course.id])
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(id=course.id).title, 'New Title')

    def test_update_moderator(self):
        course2 = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        data = {'title': 'New Title'}
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

    def test_delete_other_user(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        url = reverse('lms:course-detail', args=[course.id])
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 1)

    def test_delete_moderator(self):
        course2 = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        self.client.force_login(self.moderator)
        url = reverse('lms:course-detail', args=[course2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 1)


class TestsCRUDLesson(TestCase):

    def setUp(self):
        moder_group, _ = Group.objects.get_or_create(name='moderator')
        self.moderator = get_user_model().objects.create(email='1@1.ru', password='1234')
        self.moderator.groups.add(moder_group)
        self.user = get_user_model().objects.create(email='2@2.ru', password='1234')
        self.user2 = get_user_model().objects.create(email='3@3.ru', password='1234')

        self.moderator.save()
        self.user.save()
        self.user2.save()

        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        self.course.save()

        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Description', owner=self.user,
                                            course=self.course)
        self.lesson2 = Lesson.objects.create(title='Test Lesson', description='Test Description', owner=self.user2,
                                             course=self.course)
        self.lesson.save()
        self.lesson2.save()

    def test_delete(self):
        url = reverse('lms:lesson-delete', args=[self.lesson.id])
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_other_user(self):
        url = reverse('lms:lesson-delete', args=[self.lesson2.id])
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_moderator(self):
        url = reverse('lms:lesson-delete', args=[self.lesson2.id])
        self.client.force_login(self.moderator)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_and_check_owner(self):
        data = {'title': 'Test Lesson', 'description': 'Test Description', 'course': self.course.id}

        url = reverse('lms:lesson-create')
        self.client.force_login(self.user)
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        lesson = LessonSerializer(data=response.data)
        lesson.is_valid(raise_exception=True)
        self.assertEqual(lesson.data['owner'], self.user.id)

    def test_create_moderator(self):
        data = {'title': 'Test Lesson', 'description': 'Test Description', 'course': self.course.id}
        url = reverse('lms:lesson-create')
        self.client.force_login(self.moderator)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        data = {'title': 'New Title'}
        self.client.force_login(self.user)
        url = reverse('lms:lesson-update', args=[self.lesson.id])
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(id=self.lesson.id).title, 'New Title')

    def test_update_moderator(self):
        data = {'title': 'New Title'}
        self.client.force_login(self.moderator)
        url = reverse('lms:lesson-update', args=[self.lesson2.id])
        response = self.client.patch(url, data, 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(id=self.lesson2.id).title, 'New Title')
