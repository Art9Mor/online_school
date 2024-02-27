from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivating_user():
    time_now = timezone.now()
    user_list = User.objects.all()
    for user in user_list:
        time_away = (time_now - user.latest_login).days
        if time_away > 30:
            user.is_active = False
            user.save()
