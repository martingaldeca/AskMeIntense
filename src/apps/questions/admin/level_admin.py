from django.contrib import admin
from questions.models import Level


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "uuid",
        "name",
        "number",
        "created",
        "modified",
    ]
    list_filter = ["number"]
    search_fields = ["name", "id", "uuid", "description"]
    readonly_fields = ["uuid", "created", "modified"]
    ordering = ["created"]
