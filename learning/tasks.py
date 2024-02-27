from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_email(course, email):
    send_mail(
        subject='Online School',
        message=f'There is a new lesson in {course.name}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
