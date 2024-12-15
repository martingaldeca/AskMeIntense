from random import randint

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
    def add_level_categories(self: Question, create, extracted, **kwargs):  # pylint: disable=W0613
        from questions.factories import CategoryFactory, LevelFactory

        min_entries = kwargs.get("min", 1)
        max_entries = kwargs.get("max", 3)
        if total := kwargs.get("total", None):
            min_entries = max_entries = total
        if total != 0:
            for _ in range(randint(min_entries, max_entries)):
                self.add_level_category(level=LevelFactory(), category=CategoryFactory())  # pylint: disable=E1101


class ApprovedQuestionFactory(QuestionFactory):
    status = Question.StatusChoices.STATUS_APPROVED


class DeniedQuestionFactory(QuestionFactory):
    status = Question.StatusChoices.STATUS_DENIED
