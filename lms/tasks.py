import logging

from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest

from config.settings import env

logger = logging.getLogger(__name__)


@shared_task
def task_send_mail_for_subscribers(subject: str, message: str, email: str) -> None:
    send_mail(
        subject=subject,
        message=message,
        from_email=env.str('EMAIL_HOST_USER'),
        recipient_list=[email],
        fail_silently=False,
    )
    logger.debug(f'Send email to {email}')


def get_absolute_url(request: HttpRequest, obj: QuerySet.get) -> str:
    domain = get_current_site(request).domain
    protocol = request.scheme
    absolute_url = f'{protocol}://{domain}{obj.get_absolute_url()}'
    return absolute_url
