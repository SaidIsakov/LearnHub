from django.contrib import admin
from apps.courses.models import Course, CourseMember


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ['title', 'instructor', 'is_published', 'created_at']
  list_filter = ['is_published']
  search_fields = ['title']

@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
  list_display = ['user', 'course', 'role', 'is_active', 'enrolled_at']
  list_filter = ['role', 'is_active']
