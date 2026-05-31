from django.contrib import admin
from apps.assignments.models import Assignment, Submission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
  list_display = ['title', 'lesson', 'deadline', 'created_by']
  list_filter = ['lesson']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
  list_display = ['student', 'assignment', 'status', 'grade']
  list_filter = ['status']
