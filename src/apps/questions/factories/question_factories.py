from random import randint

from django.conf import settings
from factory import post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from questions.models import Question


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    question = FuzzyText(prefix="Question-")
    status = Question.StatusChoices.STATUS_PENDING_REVIEW
    example = FuzzyText(prefix="Example of the answer for the question-", length=150)

    @post_generation
    def add_level_categories(
        self: Question, create, extracted, **kwargs
    ):  # pylint: disable=W0613
        from questions.factories import CategoryFactory, LevelFactory

        min_entries = kwargs.get("min", 1)
        max_entries = kwargs.get("max", 3)

        if total := kwargs.get("total", None):
            min_entries = max_entries = total
        if kwargs.get("level_number"):
            min_entries = max_entries = total = 1
        if total != 0:
            for _ in range(randint(min_entries, max_entries)):
                self.add_level_category(
                    level=LevelFactory(
                        number=kwargs.get(
                            "level_number", randint(1, settings.MAX_LEVEL_ALLOWED)
                        )
                    ),
                    category=CategoryFactory(
                        name=kwargs.get("category_name", FuzzyText().fuzz())
                    ),
                )  # pylint: disable=E1101


class ApprovedQuestionFactory(QuestionFactory):
    status = Question.StatusChoices.STATUS_APPROVED


class DeniedQuestionFactory(QuestionFactory):
    status = Question.StatusChoices.STATUS_DENIED


class LikedQuestionFactory(ApprovedQuestionFactory):
    @post_generation
    def add_reaction(self, create, extracted, **kwargs):
        from questions.factories import LikedQuestionReactionFactory

        params = {"question": self}
        if user := kwargs.get("user"):
            params["user"] = user
        LikedQuestionReactionFactory(**params)


class DislikedQuestionFactory(ApprovedQuestionFactory):
    @post_generation
    def add_reaction(self, create, extracted, **kwargs):
        from questions.factories import DislikedQuestionReactionFactory

        params = {"question": self}
        if user := kwargs.get("user"):
            params["user"] = user
        DislikedQuestionReactionFactory(**params)


class FavoriteQuestionFactory(ApprovedQuestionFactory):
    @post_generation
    def add_reaction(self, create, extracted, **kwargs):
        from questions.factories import FavoriteQuestionReactionFactory

        params = {"question": self}
        if user := kwargs.get("user"):
            params["user"] = user
        FavoriteQuestionReactionFactory(**params)
