from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from learning.models import Course
from users.models import User, Subscription


class UsersTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create(
            email='testuser2@hell.ru',
            password=248
        )

        self.client.force_authenticate(user=self.owner)

        self.course = Course.objects.create(
            title='Test Course title',
            description='Test Course description',
            owner=self.owner
        )

    def test_subscription_create(self):
        """
        Test for creating a subscription
        """
        data = {
            'owner': self.owner.pk,
            'course': self.course.pk,
            'is_active': True
        }

        response = self.client.post(
            reverse('users:subscription', kwargs={'pk': self.course.pk}),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_delete(self):
        """
        Test for deleting a subscription
        """
        # data = Subscription.objects.create(
        #     owner=self.owner,
        #     course=self.course,
        #     is_active=True
        # )

        response = self.client.delete(
            reverse('users:subscription', kwargs={'pk': self.course.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
