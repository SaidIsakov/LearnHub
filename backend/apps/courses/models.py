from django.db import models
from django.conf import settings


class Course(models.Model):
  title = models.CharField(
      max_length=255
  )
  description = models.TextField(
      null=True, blank=True
  )
  instructor = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      related_name='owned_courses',
      on_delete=models.CASCADE
      )
  is_published = models.BooleanField(
      default=False
  )
  created_at = models.DateTimeField(
      auto_now_add=True
  )
  updated_at = models.DateTimeField(
      auto_now=True
  )

  def __str__(self):
      return self.title


class CourseRole(models.TextChoices):
  INSTRUCTOR = 'INSTRUCTOR', 'instructor'
  TEACHING_ASSISTANT = 'TEACHING_ASSISTANT', 'teaching_assistant'
  STUDENT = 'STUDENT', 'student'
  OBSERVER = 'OBSERVER', 'observer'


class CourseMember(models.Model):
  user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      related_name='course_memberships',
      on_delete=models.CASCADE
  )
  course = models.ForeignKey(
      Course, related_name='members',
      on_delete=models.CASCADE
  )
  role = models.CharField(
      choices=CourseRole.choices,
      default=CourseRole.STUDENT,
      max_length=20
  )
  enrolled_at = models.DateTimeField(
      auto_now_add=True
  )
  is_active = models.BooleanField(
      default=True
  )
  invited_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      null=True, blank=True,
      related_name='invited_members',
      on_delete=models.SET_NULL
  )

  class Meta:
    unique_together = ('user', 'course')

  def __str__(self):
      return self.user.username


class Lesson(models.Model):
  course = models.ForeignKey(
      Course,
      related_name='lessons',
      on_delete=models.CASCADE
  )
  title = models.CharField(
      max_length=255
  )
  content = models.TextField(
      blank=True,
      null=True
  )
  order = models.PositiveIntegerField(
      default=0
  )
  is_published = models.BooleanField(
      default=False
  )
  created_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      related_name='lessons',
      on_delete=models.CASCADE
  )
  created_at = models.DateTimeField(
      auto_now_add=True
  )
  updated_at = models.DateTimeField(
      auto_now=True
  )

  class Meta:
    ordering = ['order']

  def __str__(self):
      return self.title


class ChatMessage(models.Model):
  lesson = models.ForeignKey(
      Lesson,
      on_delete=models.CASCADE,
      related_name='chat_messages'
  )
  user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name='chat_messages'
  )
  question = models.TextField()
  answer = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.question[:50]

  class Meta:
    ordering = ['-created_at']
