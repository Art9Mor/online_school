from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from learning.models import Course, Lesson
from users.models import User


class LearningTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='testuser@hell.ru',
        )
        self.user.set_password('666')

        # access_token = str(RefreshToken.for_user(self.user).access_token)
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer' + access_token)

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='TestTitle',
            description='TestDescription',
            owner=self.user
        )

    def test_lesson_create(self):
        """
        Test creating a lesson
        """
        data = {
            'title': 'TestTitle',
            'description': 'TestDescription',
            'owner': self.user.id,
            'course': self.course.id,
            'video': 'https://www.youtube.com/watch?v=9Bm-kdLwBVc&ab_channel=drakkon8'
        }

        response = self.client.post(
            reverse('learning:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_lesson_list(self):
        """
        Test listing all lessons for a specific course
        """
        response = self.client.get(
            reverse('learning:lesson_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_create_validation_error(self):
        """
        Test creating a lesson with invalid data
        """
        data = {
            'title': 'Test2Title',
            'description': 'Test2Description',
            'owner': self.user.pk,
            'course': self.course.pk,
            'video': 'https://vk.com/video?q=Burzum&z=video155225046_456242150%2Fpl_cat_trends'
        }
        response = self.client.post(
            reverse('learning:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Недопустимая ссылка.']}
        )
