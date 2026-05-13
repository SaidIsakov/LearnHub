from rest_framework import serializers
from apps.courses.models import Course, Lesson


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
