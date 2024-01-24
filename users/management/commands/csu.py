from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='online_school@yandex.ru',
            first_name='Ad',
            last_name='Min',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password('666')
        user.save()
