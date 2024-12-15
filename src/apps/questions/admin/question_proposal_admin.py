from core.helpers import get_admin_reference
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from questions.models import QuestionProposal


@admin.register(QuestionProposal)
class QuestionProposalAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "uuid",
        "get_question",
        "get_proposing_user",
        "question__status",
        "created",
        "modified",
    ]
    list_filter = ["question__status"]
    search_fields = [
        "id",
        "uuid",
        "question__id",
        "question__uuid",
        "proposing_user__id",
        "proposing_user__uuid",
        "proposing_user__email",
    ]
    readonly_fields = ["uuid", "created", "modified"]
    raw_id_fields = ["question", "proposing_user"]
    ordering = ["created"]

    def get_question(self, obj: QuestionProposal):
        return get_admin_reference(obj.question)

    get_question.short_description = _("Question")

    def get_proposing_user(self, obj: QuestionProposal):
        return get_admin_reference(obj.proposing_user)

    get_proposing_user.short_description = _("Proposing user")
