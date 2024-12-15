from core.factories import UserFactory
from factory import SubFactory
from factory.django import DjangoModelFactory
from questions.factories import QuestionFactory
from questions.models import QuestionProposal


class QuestionProposalFactory(DjangoModelFactory):
    class Meta:
        model = QuestionProposal

    question = SubFactory(QuestionFactory)
    proposing_user = SubFactory(UserFactory)
