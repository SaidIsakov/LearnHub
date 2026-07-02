from django.contrib import admin
from apps.users.models import User, AIRecommendation



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ['username', 'telegram_id']
  search_fields = ['telegram_id']


@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
  list_display = ['user', 'strengths', 'weaknesses']
