from django.conf import settings
from django.core.management import BaseCommand

from config.settings import BASE_DIR
from users.services import create_webhook


class Command(BaseCommand):
    help = 'Создание и получение секретного ключа для webhook'

    def handle(self, *args, **options):
        if settings.STRIPE_SECRET_WEBHOOK is not None:
            print('Переменная STRIPE_SECRET_WEBHOOK уже существует')
            return

        web_hook = create_webhook()
        STRIPE_SECRET_WEBHOOK = web_hook.get('secret')
        print(f'Секретный ключ для webhook: {STRIPE_SECRET_WEBHOOK}')
        user_input = input('Записать в .env-файл переменную STRIPE_SECRET_WEBHOOK? (y/n): ').lower()
        path_to_env = BASE_DIR / '.env'
        if user_input in {'y', 'yes'}:
            with open(path_to_env, 'a', encoding='utf-8') as file:
                print(f'\nSTRIPE_SECRET_WEBHOOK={STRIPE_SECRET_WEBHOOK}', file=file)
