from rest_framework import serializers
from apps.courses.models import Course, Lesson, CourseMember


class CourseSerializer(serializers.ModelSerializer):
  instructor = serializers.PrimaryKeyRelatedField(read_only=True)
  class Meta:
    model = Course
    fields = ['id', 'title', 'description', 'instructor', 'is_published', 'created_at']


class LessonSerializer(serializers.ModelSerializer):
  created_by = serializers.PrimaryKeyRelatedField(read_only=True)
  class Meta:
    model = Lesson
    fields = ['id', 'course', 'title', 'content', 'order', 'is_published', 'created_by', 'created_at']
    read_only_fields = ['course', 'created_by']


class CourseMemberSerializer(serializers.ModelSerializer):
  enrolled_at = serializers.DateTimeField(read_only=True)
  invited_by = serializers.PrimaryKeyRelatedField(read_only=True)
  course = serializers.PrimaryKeyRelatedField(read_only=True)
  class Meta:
    model = CourseMember
    fields = ['id', 'user', 'course', 'role', 'enrolled_at', 'is_active',
        'invited_by']

