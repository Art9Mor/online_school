from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from learning.models import Course, Lesson
from learning.permissions import IsOwnerStaff
from learning.serializers import *


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    default_serializer = CourseSerializer
    serializers = {
        'list': CourseListSerializer,
        'retrieve': CourseDetailSerializer,
    }

    def perform_create(self, serializer):
        """
        Create a new course and assign it to the current user
        """
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwnerStaff]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwnerStaff]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwnerStaff]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)


class LessonCreateAPIVIew(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """
        Create a new lesson instance and assign it to the current owner
        """
        new_lesson = serializer.save(user=self.request.user)
        new_lesson.save()


class LessonListAPIVIew(generics.ListAPIView):
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerStaff]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerStaff]


class CourseLessonsListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.filter(course__isnull=False)
    serializer_class = CourseLessonSerializer
    permission_classes = [IsOwnerStaff]
