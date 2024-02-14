from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from learning.models import Course, Lesson
from learning.permissions import IsModer, IsOwner
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
        new_course = serializer.save(owner=self.request.user)
        new_course.save()

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ('update', 'retrieve'):
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)


class LessonCreateAPIVIew(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModer]

    def perform_create(self, serializer):
        """
        Create a new lesson instance and assign it to the current owner
        """
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.save()


class LessonListAPIVIew(generics.ListAPIView):
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'course__name', 'owner__username']
    ordering_fields = ['id',]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModer]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModer]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class CourseLessonsListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.filter(course__isnull=False)
    serializer_class = CourseLessonSerializer
    permission_classes = [IsOwner | IsModer]
