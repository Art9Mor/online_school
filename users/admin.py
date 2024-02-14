from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ('password',)
