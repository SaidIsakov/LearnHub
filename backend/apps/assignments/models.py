from django.db import models
from apps.courses.models import Lesson
from django.conf import settings


class AssignmentStatus(models.TextChoices):
  PENDING = 'pending', 'Не сдано'
  SUBMITTED = 'submitted', 'Сдано'
  REVIEWED = 'reviewed', 'Проверено'

class Assignment(models.Model):
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
      related_name='assignments'
  )
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  deadline = models.DateTimeField(null=True, blank=True)
  created_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name='assignments'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.title


class Submission(models.Model):
  assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,
      related_name='submissions'
  )
  student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
      related_name='submissions'
  )
  content = models.TextField()
  status = models.CharField(
      choices=AssignmentStatus.choices,
      default=AssignmentStatus.PENDING,
      max_length=20
  )
  grade = models.PositiveIntegerField(null=True, blank = True)
  submitted_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ('assignment', 'student')

  def __str__(self):
      return f'{self.student} - {self.assignment}'

