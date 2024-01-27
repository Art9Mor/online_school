from rest_framework import serializers

from learning.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj.id).count()

    # def create(self, validated_data):
    #     lessons_data = validated_data.pop('lessons')
    #     course = Course.objects.create(**validated_data)
    #     for lesson_data in lessons_data:
    #         return Lesson.objects.create(course=course, **lesson_data)
    #     return course


class CourseLessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = ('title', 'description')
