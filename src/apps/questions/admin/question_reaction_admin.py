from core.helpers import get_admin_reference
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from questions.models import QuestionReaction


@admin.register(QuestionReaction)
class QuestionReactionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "uuid",
        "get_question",
        "get_user",
        "reaction",
        "created",
        "modified",
    ]
    list_filter = ["reaction"]
    search_fields = [
        "id",
        "uuid",
        "question__id",
        "question__uuid",
        "user__id",
        "user__uuid",
        "user__email",
    ]
    readonly_fields = ["uuid", "created", "modified"]
    raw_id_fields = ["question", "user"]
    ordering = ["created"]

    def get_question(self, obj: QuestionReaction):
        return get_admin_reference(obj.question)

    get_question.short_description = _("Question")

    def get_user(self, obj: QuestionReaction):
        return get_admin_reference(obj.user)

    get_user.short_description = _("User")
