from core.helpers import get_admin_image
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from questions.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "uuid",
        "name",
        "get_category_icon",
        "created",
        "modified",
    ]
    search_fields = ["name", "id", "uuid", "description"]
    readonly_fields = ["uuid", "created", "modified"]
    ordering = ["created"]

    def get_category_icon(self, obj):
        return get_admin_image(obj=obj, picture_field="icon", size=50)

    get_category_icon.short_description = _("Icon")
