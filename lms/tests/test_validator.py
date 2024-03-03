from django.contrib.auth import get_user_model
from django.db.models import signals
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from lms.models import Course


class CheckLinkVideoTestCase(TestCase):

    def setUp(self):
        signals.post_save.disconnect(sender=Course, dispatch_uid='Course_post_save')

        self.user = get_user_model().objects.create(email='1@1.ru', password='1234')
        self.user.save()

    def test_create(self):
        course = Course.objects.create(title='JS', description='very cool')
        data = {
            "title": "Test",
            "description": "Desc test",
            "link_video": "",
            "course": course.id,
            "owner": self.user.id,
        }
        self.client.force_login(self.user)
        url = reverse('lms:lesson-create')

        good_data = ['', None, 'https://www.youtube.com', 'https://www.youtube.com/']
        bad_data = ['123', 'www.youtube.com', 'https://', 1, [], (1, 2)]

        self.replace_and_get_response(url, data, good_data, status.HTTP_201_CREATED)
        self.replace_and_get_response(url, data, bad_data, status.HTTP_400_BAD_REQUEST)

    def replace_and_get_response(self, url, data, data_set, status_):
        for link_video in data_set:
            data['link_video'] = link_video
            response = self.client.post(url, data, 'application/json')
            self.assertEqual(response.status_code, status_)
