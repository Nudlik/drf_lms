from datetime import timedelta

from django.apps import AppConfig


class LmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms'
    verbose_name = 'Онлайн-обучение'
    TIME_COOLDOWN = timedelta(hours=4)

    def ready(self):
        import lms.signals
