from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from learning.models import Course
from users.models import User, Subscription


class UsersTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='testuser2@hell.ru',
            password=248
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Test Course title',
            description='Test Course description',
            owner=self.user
        )

    def test_subscription_create(self):
        data = {
            'owner': self.user.pk,
            'course': self.course.pk,
            'is_active': True
        }

        response = self.client.post(
            reverse('users:subscription_create', kwargs={'pk': self.course.pk}),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_delete(self):
        data = Subscription.objects.create(
            owner=self.user,
            course=self.course
        )

        response = self.client.delete(
            reverse('users:subscription_delete', kwargs={'pk': self.course.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
