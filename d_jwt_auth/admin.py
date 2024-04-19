from django.contrib import admin

from .models import UserAuth


@admin.register(UserAuth)
class UserAuthModelAdmin(admin.ModelAdmin):
    pass
