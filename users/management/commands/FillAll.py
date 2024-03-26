from django.core.management.base import BaseCommand

from users.management.commands.csu import Command as CSUCommand
from users.management.commands.fill_payment import Command as FillPaymentCommand
from users.management.commands.fill_user import Command as FillUserCommand


class Command(BaseCommand):
    help = 'Активация всех команд на заполнение'

    def handle(self, *args, **options):
        # Создание суперпользователя
        create_superuser = CSUCommand()
        create_superuser.handle(*args, **options)

        # Создание заполнения оплаты
        fill_payment = FillPaymentCommand()
        fill_payment.handle(*args, **options)

        # Создание заполнения пользователей
        fill_user = FillUserCommand()
        fill_user.handle(*args, **options)
