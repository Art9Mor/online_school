from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from learning.models import Course, Lesson
from learning.permissions import IsOwnerStaff, IsOwner, IsModerator
from learning.serializers import CourseSerializer, LessonSerializer, CourseLessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]


class LessonCreateAPIVIew(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """
        Create a new lesson instance and assign it to the current owner
        """
        new_lesson = serializer.save(user=self.request.user)
        new_lesson.save()


class LessonListAPIVIew(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


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
    permission_classes = [IsOwner]


class CourseLessonsListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.filter(course__isnull=False)
    serializer_class = CourseLessonSerializer
