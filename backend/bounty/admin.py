from django.contrib import admin

from .models import HuntLog, WantedCriminal


@admin.register(WantedCriminal)
class WantedCriminalAdmin(admin.ModelAdmin):
    list_display = ["nickname", "name", "reward", "difficulty", "armed", "has_crew", "escape_master"]
    list_filter = ["armed", "has_crew", "escape_master", "difficulty"]


@admin.register(HuntLog)
class HuntLogAdmin(admin.ModelAdmin):
    list_display = ["id", "criminal", "success", "created_at"]
    list_filter = ["success"]
