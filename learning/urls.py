from django.urls import path

from rest_framework.routers import DefaultRouter

from learning.apps import LearningConfig
from learning.views import CourseViewSet, LessonCreateAPIVIew, LessonListAPIVIew, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, CourseLessonsListAPIView

app_name = LearningConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIVIew.as_view(), name='lesson_create'),
                  path('lesson/', LessonListAPIVIew.as_view(), name='lesson_list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
                  path('course/lesson/', CourseLessonsListAPIView.as_view(), name='course_lesson'),
              ] + router.urls
