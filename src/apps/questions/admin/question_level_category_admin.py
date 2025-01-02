from core.helpers import get_admin_reference
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from questions.models import QuestionLevelCategory


@admin.register(QuestionLevelCategory)
class QuestionLevelCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "uuid",
        "get_question",
        "get_level",
        "get_category",
        "order",
        "created",
        "modified",
    ]
    list_filter = ["category", "level", "order"]
    raw_id_fields = ["question", "level", "category"]
    search_fields = [
        "id",
        "uuid",
        "level__id",
        "level__uuid",
        "level__name",
        "category__id",
        "category__uuid",
        "category__name",
    ]
    readonly_fields = ["uuid", "created", "modified"]
    ordering = ["created"]

    def get_question(self, obj):
        return get_admin_reference(obj.question)

    get_question.short_description = _("Question")

    def get_category(self, obj):
        return get_admin_reference(obj.category)

    get_category.short_description = _("Category")

    def get_level(self, obj):
        return get_admin_reference(obj.level)

    get_level.short_description = _("Level")
