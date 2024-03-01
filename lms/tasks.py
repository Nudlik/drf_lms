import logging

from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse

from config.settings import env

logger = logging.getLogger(__name__)


@shared_task
def task_send_mail_for_subscribers(url, title, email):
    send_mail(
        subject=f'В курс "{title}" добавился новый контент',
        message=f'Перейдите по ссылке для просмотра {url}',
        from_email=env.str('EMAIL_HOST_USER'),
        recipient_list=[email],
        fail_silently=False,
    )
    logger.debug(f'Send email to {email}')


def get_data_for_email(request, obj, email):
    site = get_current_site(request)
    post_url = reverse('lms:course-detail', args=[obj.pk])
    absolute_url = f'{request.scheme}://{site.domain}{post_url}'
    return absolute_url, obj.title, email
