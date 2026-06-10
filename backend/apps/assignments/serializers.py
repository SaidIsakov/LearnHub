from rest_framework import serializers
from apps.assignments.models import Assignment, Submission


class AssignmentSerializer(serializers.ModelSerializer):
  created_by = serializers.PrimaryKeyRelatedField(read_only=True)
  lesson = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Assignment
    fields = ['id', 'lesson', 'title', 'description', 'deadline', 'created_by',
        'created_at'
    ]


class SubmissionSerializer(serializers.ModelSerializer):
  student = serializers.PrimaryKeyRelatedField(read_only=True)
  submitted_at = serializers.DateTimeField(read_only=True)
  grade = serializers.IntegerField(read_only=True)

  class Meta:
    model = Submission
    fields = ['id', 'assignment', 'student', 'content', 'status',
        'grade', 'submitted_at',
    ]
