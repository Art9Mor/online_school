from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from learning.paginators import LearningPaginator
from users.permissions import IsModer, IsOwner
from learning.serializers import *


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    default_serializer = CourseSerializer
    pagination_class = LearningPaginator
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
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
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
    pagination_class = LearningPaginator
    queryset = Lesson.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'course__name', 'owner__username']
    ordering_fields = ['id', ]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class CourseLessonsListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.filter(course__isnull=False)
    serializer_class = CourseLessonSerializer
    pagination_class = LearningPaginator
    permission_classes = [IsAuthenticated, IsOwner | IsModer]

