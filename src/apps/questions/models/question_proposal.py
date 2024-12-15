import logging

from core.models import TimeStampedUUIDModel, User
from django.db import models
from django.utils.translation import gettext_lazy as _
from questions.models import Question

logger = logging.getLogger(__name__)


class QuestionProposal(TimeStampedUUIDModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Question"),
        help_text=_("Question answered by the user"),
        db_index=True,
    )
    proposing_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Proposing user"),
        help_text=_("User that proposed the question"),
        related_name="proposals",
        related_query_name="proposals",
        db_index=True,
    )

    class Meta:
        verbose_name = _("Question proposal")
        verbose_name_plural = _("Question proposals")
