import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import Payments


class MyTest(APITestCase):

    @patch('stripe.Webhook.construct_event')
    def test_webhook(self, mock_construct_event):
        user = self.user = get_user_model().objects.create(email='2@2.ru', password='1234')
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user, price=100)

        payment = Payments.objects.create(
            session_id='cs_test_a1RlCamvk3nDRrxKWNyDCPcsxpMnZkAfavbvAMfbbcWKjgqIyJv7U5Gzsa',
            url='session.url',
            user=user,
            course=course
        )
        payment.save()

        url = reverse('users:webhook')
        with open('users/tests/test_data/event_test_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        headers = {'STRIPE_SIGNATURE': 'test_signature'}

        # подменяем функцию construct_event
        mock_construct_event.return_value = data

        response = self.client.post(url, data, format='json', headers=headers)
        session = data['data']['object']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})
        self.assertEqual(Payments.objects.count(), 1)

        payment = Payments.objects.first()
        self.assertTrue(payment.payed)
        self.assertAlmostEquals(payment.payment_amount, session['amount_total'] / 100, 2)
