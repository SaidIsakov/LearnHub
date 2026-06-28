from django.contrib import admin
from apps.courses.models import Course, CourseMember, Lesson, ChatMessage


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ['title', 'instructor', 'is_published', 'created_at']
  list_filter = ['is_published']
  search_fields = ['title']

@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
  list_display = ['user', 'course', 'role', 'is_active', 'enrolled_at']
  list_filter = ['role', 'is_active']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
  list_display = ['title', 'course', 'order', 'is_published', 'created_by']
  list_filter = ['is_published', 'course']
  search_fields = ['title']
  ordering = ['order']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
  list_display = ['user', 'question']
  list_filter = ['lesson']

