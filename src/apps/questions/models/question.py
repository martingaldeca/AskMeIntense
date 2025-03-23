import logging

from core.models import TimeStampedUUIDModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from questions.exceptions import NotValidQuestionStatusForApproveOrDeny
from questions.models import Category, Level
from questions.models.managers import CustomQuestionManager

logger = logging.getLogger(__name__)


class Question(TimeStampedUUIDModel):
    class StatusChoices(models.TextChoices):
        STATUS_APPROVED = ["APPROVED", _("APPROVED")]
        STATUS_DENIED = ["DENIED", _("DENIED")]
        STATUS_PENDING_REVIEW = ["PENDING_REVIEW", _("PENDING_REVIEW")]

    question = models.TextField(
        verbose_name=_("Question"),
        help_text=_(
            "Question text, this is the main question that will appear to the asker"
        ),
    )
    status = models.CharField(
        max_length=255,
        verbose_name=_("Status"),
        help_text=_("The status of the question"),
        choices=StatusChoices,
        default=StatusChoices.STATUS_PENDING_REVIEW,
    )
    example = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Example"),
        help_text=_("Example of one valid answer for the question"),
    )
    categories = models.ManyToManyField(
        Category, through="QuestionLevelCategory", verbose_name=_("Categories")
    )
    levels = models.ManyToManyField(
        Level, through="QuestionLevelCategory", verbose_name=_("Levels")
    )

    objects = CustomQuestionManager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def approve(self):
        if self.status != self.StatusChoices.STATUS_PENDING_REVIEW:
            raise NotValidQuestionStatusForApproveOrDeny(self)
        self.status = Question.StatusChoices.STATUS_APPROVED
        self.save()

    def deny(self):
        if self.status != self.StatusChoices.STATUS_PENDING_REVIEW:
            raise NotValidQuestionStatusForApproveOrDeny(self)
        self.status = Question.StatusChoices.STATUS_DENIED
        self.save()

    def add_level_category(self, level: Level, category: Category):
        from questions.models import QuestionLevelCategory

        QuestionLevelCategory.objects.create(
            question=self,
            category=category,
            level=level,
        )

    def _react(self, reaction, user):
        from questions.models import QuestionReaction

        if reaction not in QuestionReaction.ReactionChoices.values:
            raise ValueError("Reaction not valid")
        QuestionReaction.objects.create(
            question=self,
            reaction=reaction,
            user=user,
        )

    def react_like(self, user):
        from questions.models import QuestionReaction

        self._remove_reaction(QuestionReaction.ReactionChoices.DISLIKE, user)
        self._react(QuestionReaction.ReactionChoices.LIKE, user)

    def react_dislike(self, user):
        from questions.models import QuestionReaction

        self._remove_reaction(QuestionReaction.ReactionChoices.LIKE, user)
        self._react(QuestionReaction.ReactionChoices.DISLIKE, user)

    def react_favorite(self, user):
        from questions.models import QuestionReaction

        self._react(QuestionReaction.ReactionChoices.FAVORITE, user)

    def _remove_reaction(self, reaction, user):
        from questions.models import QuestionReaction

        if reaction not in QuestionReaction.ReactionChoices.values:
            raise ValueError("Reaction not valid")
        self.reactions.filter(
            question=self,
            user=user,
            reaction=reaction,
        ).delete()

    def remove_like(self, user):
        from questions.models import QuestionReaction

        self._remove_reaction(QuestionReaction.ReactionChoices.LIKE, user)

    def remove_dislike(self, user):
        from questions.models import QuestionReaction

        self._remove_reaction(QuestionReaction.ReactionChoices.DISLIKE, user)

    def remove_favorite(self, user):
        from questions.models import QuestionReaction

        self._remove_reaction(QuestionReaction.ReactionChoices.FAVORITE, user)
