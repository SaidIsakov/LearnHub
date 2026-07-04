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
  summary = models.CharField()
  strengths = ArrayField(
      models.CharField(
          default=list
      )
  )
  weaknesses = ArrayField(
      models.CharField(
          default=list
      )
  )
  next_goal = models.TextField()
  motivation = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return f"Recommendation for {self.user.username}"
