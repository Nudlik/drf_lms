import logging
from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def deactivate_inactive_users():
    users = get_user_model().objects.filter(is_active=True, last_login__lte=timezone.now() - timedelta(days=30))
    logger.debug(f'{len(users)} пользователей заблокировало\nПользователи: {users}')
    users.update(is_active=False)
