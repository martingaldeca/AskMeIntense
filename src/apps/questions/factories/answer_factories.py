from core.factories import UserFactory
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from questions.factories import QuestionFactory
from questions.models import Answer


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    question = SubFactory(QuestionFactory)
    answer = FuzzyText()
    asker = SubFactory(UserFactory)
    respondent = SubFactory(UserFactory)
