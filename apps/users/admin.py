from django.contrib import admin

from .models import User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_active', 'is_staff')
    clickable_fields = ('username', 'email', 'phone')