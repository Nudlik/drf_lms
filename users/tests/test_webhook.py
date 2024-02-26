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
        data = {'api_version': '2023-10-16',
                'created': 1708963244,
                'data': {'object': {'after_expiration': None,
                                    'allow_promotion_codes': None,
                                    'amount_subtotal': 25000,
                                    'amount_total': 25000,
                                    'automatic_tax': {'enabled': False,
                                                      'liability': None,
                                                      'status': None},
                                    'billing_address_collection': None,
                                    'cancel_url': 'http://127.0.0.1:8000/users/buy/canceled/',
                                    'client_reference_id': None,
                                    'client_secret': None,
                                    'consent': None,
                                    'consent_collection': None,
                                    'created': 1708963112,
                                    'currency': 'rub',
                                    'currency_conversion': None,
                                    'custom_fields': [],
                                    'custom_text': {'after_submit': None,
                                                    'shipping_address': None,
                                                    'submit': None,
                                                    'terms_of_service_acceptance': None},
                                    'customer': None,
                                    'customer_creation': 'if_required',
                                    'customer_details': {'address': {'city': None,
                                                                     'country': 'RU',
                                                                     'line1': None,
                                                                     'line2': None,
                                                                     'postal_code': None,
                                                                     'state': None},
                                                         'email': '123@mail.ru',
                                                         'name': '42',
                                                         'phone': None,
                                                         'tax_exempt': 'none',
                                                         'tax_ids': []},
                                    'customer_email': None,
                                    'expires_at': 1709049512,
                                    'id': 'cs_test_a1RlCamvk3nDRrxKWNyDCPcsxpMnZkAfavbvAMfbbcWKjgqIyJv7U5Gzsa',
                                    'invoice': None,
                                    'invoice_creation': {'enabled': False,
                                                         'invoice_data': {'account_tax_ids': None,
                                                                          'custom_fields': None,
                                                                          'description': None,
                                                                          'footer': None,
                                                                          'issuer': None,
                                                                          'metadata': {},
                                                                          'rendering_options': None}},
                                    'livemode': False,
                                    'locale': None,
                                    'metadata': {'hello': 'world', 'product_id': '1'},
                                    'mode': 'payment',
                                    'object': 'checkout.session',
                                    'payment_intent': 'pi_3Oo6beDrMzhPj0Qt4Uf5YTqt',
                                    'payment_link': None,
                                    'payment_method_collection': 'if_required',
                                    'payment_method_configuration_details': None,
                                    'payment_method_options': {},
                                    'payment_method_types': ['card'],
                                    'payment_status': 'paid',
                                    'phone_number_collection': {'enabled': False},
                                    'recovered_from': None,
                                    'setup_intent': None,
                                    'shipping_address_collection': None,
                                    'shipping_cost': None,
                                    'shipping_details': None,
                                    'shipping_options': [],
                                    'status': 'complete',
                                    'submit_type': None,
                                    'subscription': None,
                                    'success_url': 'http://127.0.0.1:8000/users/buy/success/',
                                    'total_details': {'amount_discount': 0,
                                                      'amount_shipping': 0,
                                                      'amount_tax': 0},
                                    'ui_mode': 'hosted',
                                    'url': None}},
                'id': 'evt_1Oo6bgDrMzhPj0QtjyESz5GG',
                'livemode': False,
                'object': 'event',
                'pending_webhooks': 1,
                'request': {'id': None, 'idempotency_key': None},
                'type': 'checkout.session.completed'}
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
