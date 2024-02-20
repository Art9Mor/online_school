from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from learning.models import Course, Lesson
from learning.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='video')]


class LessonListSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('title', 'course')


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj.id).count()

    def get_is_subscribed(self, obj):
        owner = self.context['request'].user
        is_subscribed = Subscription.objects.filter(course=obj.id, user=owner).exists()
        return is_subscribed

    # def create(self, validated_data):
    #     lessons_data = validated_data.pop('lessons')
    #     course = Course.objects.create(**validated_data)
    #     for lesson_data in lessons_data:
    #         return Lesson.objects.create(course=course, **lesson_data)
    #     return course


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_in_course = SerializerMethodField()

    def get_lessons_in_course(self, course):
        return LessonListSerializer(Lesson.objects.filter(course=course), many=True).data

    class Meta:
        model = Course
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title',)


class CourseLessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = ('title', 'description')
