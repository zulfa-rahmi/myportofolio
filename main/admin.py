from django.contrib import admin

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "category", "started_at", "ended_at")
    list_filter = ("category",)
    search_fields = ("title", "organization", "description")

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "event", "year")
    search_fields = ("title", "event", "description")
    ordering = ("-year",)
