from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type', 'is_active')
    list_editable = ('user_type', 'is_active')
