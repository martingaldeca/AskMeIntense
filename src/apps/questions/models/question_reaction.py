import logging

from core.models import TimeStampedUUIDModel, User
from django.db import models
from django.utils.translation import gettext_lazy as _
from questions.models import Question
from questions.models.managers import CustomQuestionReactionManager

logger = logging.getLogger(__name__)


class QuestionReaction(TimeStampedUUIDModel):
    class ReactionChoices(models.TextChoices):
        LIKE = ["LIKE", _("Like")]
        DISLIKE = ["DISLIKE", _("Dislike")]
        FAVORITE = ["FAVORITE", _("Favorite")]

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Question"),
        help_text=_("Question the user has reacted to."),
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("User that has reacted to the question."),
        related_name="reactions",
        related_query_name="reactions",
        db_index=True,
    )
    reaction = models.CharField(
        max_length=255,
        verbose_name=_("Reaction"),
        help_text=_("Reaction of the user to the question."),
        choices=ReactionChoices,
        default=ReactionChoices.LIKE,
    )
    objects = CustomQuestionReactionManager()

    class Meta:
        verbose_name = _("Question reaction")
        verbose_name_plural = _("Question reactions")
