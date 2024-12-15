from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from questions.models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "uuid",
        "asker",
        "question",
        "short_answer",
        "respondent",
        "created",
        "modified",
    ]
    search_fields = [
        "id",
        "uuid",
        "asker__id",
        "asker__uuid",
        "asker__email",
        "question__id",
        "question__uuid",
        "respondent__id",
        "respondent__uuid",
        "respondent__email",
    ]
    readonly_fields = ["uuid", "created", "modified"]
    raw_id_fields = ["asker", "question", "respondent"]
    ordering = ["created"]

    def short_answer(self, obj: Answer):
        return (
            f"{obj.answer[:settings.ADMIN_SHORT_TEXT_LENGTH]}"
            f"{'...' if len(obj.answer) > settings.ADMIN_SHORT_TEXT_LENGTH else ''}"
        )

    short_answer.short_description = _("Answer")
