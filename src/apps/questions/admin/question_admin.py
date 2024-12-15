from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from questions.exceptions import NotValidQuestionStatusForApproveOrDeny
from questions.models import Question


class LevelCategoriesInline(admin.TabularInline):
    model = Question.categories.through  # pylint: disable=E1101


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "uuid",
        "short_question",
        "status",
        "short_example",
        "created",
        "modified",
    ]
    list_filter = ["status"]
    search_fields = ["question", "id", "uuid", "example"]
    readonly_fields = ["uuid", "created", "modified"]
    ordering = ["created"]
    inlines = [LevelCategoriesInline]
    actions = ["approve_questions", "deny_questions"]

    def short_question(self, obj: Question):
        return (
            f"{obj.question[:settings.ADMIN_SHORT_TEXT_LENGTH]}"
            f"{'...' if len(obj.question) > settings.ADMIN_SHORT_TEXT_LENGTH else ''}"
        )

    short_question.short_description = _("Question")

    def short_example(self, obj: Question):
        return (
            f"{obj.example[:settings.ADMIN_SHORT_TEXT_LENGTH]}"
            f"{'...' if len(obj.example) > settings.ADMIN_SHORT_TEXT_LENGTH else ''}"
        )

    short_example.short_description = _("Example")

    def _process_questions(self, request, queryset, action, success_verb, error_message, verb_termination):
        success_count = 0
        problem_count = 0

        for question in queryset:
            try:
                action(question)
                success_count += 1
            except NotValidQuestionStatusForApproveOrDeny:
                problem_count += 1

        if problem_count > 0:
            error_message_formatted = format_html(
                _(
                    f"<strong>{problem_count}</strong> "
                    f"question{'s' if problem_count != 1 else ''} "
                    f"could not be {success_verb}{verb_termination}. {error_message}"
                )
            )
            self.message_user(request, _(error_message_formatted), level=messages.ERROR)

        if success_count > 0:
            success_message = format_html(
                _(
                    f"<strong>{success_count}</strong> "
                    f"question{'s' if success_count != 1 else ''} "
                    f"{success_verb}{verb_termination}."
                )
            )
            self.message_user(request, _(success_message), level=messages.INFO)
        return HttpResponseRedirect(request.get_full_path())

    def approve_questions(self, request, queryset):
        return self._process_questions(
            request,
            queryset,
            action=lambda question: question.approve(),
            success_verb="approve",
            verb_termination=_("d"),
            error_message=_("You can only approve pending questions."),
        )

    approve_questions.short_description = _("Approve selected questions")

    def deny_questions(self, request, queryset):
        return self._process_questions(
            request,
            queryset,
            action=lambda question: question.deny(),
            success_verb="denie",
            verb_termination=_("d"),
            error_message=_("You can only deny pending questions."),
        )

    deny_questions.short_description = _("Deny selected questions")
