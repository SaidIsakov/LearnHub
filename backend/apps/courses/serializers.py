from rest_framework import serializers
from apps.courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
  instructor = serializers.PrimaryKeyRelatedField(read_only=True)
  class Meta:
    model = Course
    fields = ['id', 'title', 'description', 'instructor', 'is_published', 'created_at']
