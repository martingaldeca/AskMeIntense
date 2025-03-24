import logging

from core.models import TimeStampedUUIDModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from questions.models import Category, Level, Question

logger = logging.getLogger(__name__)


class QuestionLevelCategory(TimeStampedUUIDModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Question"),
        help_text=_("This is the question related to a level and a category"),
        related_name="levels_and_categories",
        related_query_name="levels_and_categories",
        db_index=True,
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        verbose_name=_("Level"),
        help_text=_("This is the level related to a question and a category"),
        related_name="questions_and_categories",
        related_query_name="questions_and_categories",
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("Category"),
        help_text=_("This is the category related to a question and a level"),
        related_name="questions_and_levels",
        related_query_name="questions_and_levels",
        db_index=True,
    )
    order = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Order"),
        help_text=_("Order of the question in the level and category."),
    )

    class Meta:
        verbose_name = _("Question level category")
        verbose_name_plural = _("Question level categories")
        unique_together = [["question", "level", "category"]]
        indexes = [
            models.Index(fields=["level", "category"]),
        ]
