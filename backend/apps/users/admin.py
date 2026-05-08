from django.contrib import admin
from apps.users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ['username', 'telegram_id']
  search_fields = ['telegram_id']
