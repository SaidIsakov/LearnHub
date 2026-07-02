from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
  telegram_id = models.BigIntegerField(
      unique=True,
      null=True,
      blank=True,
      verbose_name='Telegram Id'
  )


class AIRecommendation(models.Model):
  user = models.OneToOneField(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name='recommendations'
  )
  summary = models.CharField(max_length=200)
  strengths = ArrayField(
      models.CharField(
          max_length=100,
          default=list
      )
  )
  weaknesses = ArrayField(
      models.CharField(
          max_length=100,
          default=list
      )
  )
  next_goal = models.TextField(max_length=200)
  motivation = models.TextField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return f"Recommendation for {self.user.username}"
