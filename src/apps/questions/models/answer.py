import logging

from core.models import TimeStampedUUIDModel, User
from django.db import models
from django.utils.translation import gettext_lazy as _
from questions.models import Question

logger = logging.getLogger(__name__)


class Answer(TimeStampedUUIDModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Question"),
        help_text=_("Question answered by the user"),
        related_name="answers",
        related_query_name="answers",
        db_index=True,
    )
    answer = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Answer"),
        help_text=_("Answer to the question given by the respondant"),
    )
    asker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Asker"),
        help_text=_("Asker of the question"),
        related_name="asked_questions_answers",
        related_query_name="asked_questions_answers",
        db_index=True,
    )
    respondent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Respondent"),
        help_text=_("Respondent of the question"),
        related_name="answered_questions_answers",
        related_query_name="answered_questions_answers",
        db_index=True,
    )

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
