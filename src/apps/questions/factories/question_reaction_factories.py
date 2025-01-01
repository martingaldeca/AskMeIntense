from core.factories import UserFactory
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from questions.factories import QuestionFactory
from questions.models import QuestionReaction


class QuestionReactionFactory(DjangoModelFactory):
    class Meta:
        model = QuestionReaction

    question = SubFactory(QuestionFactory)
    user = SubFactory(UserFactory)
    reaction = FuzzyChoice(QuestionReaction.ReactionChoices.choices)


class LikedQuestionReactionFactory(QuestionReactionFactory):
    reaction = QuestionReaction.ReactionChoices.LIKE


class DislikedQuestionReactionFactory(QuestionReactionFactory):
    reaction = QuestionReaction.ReactionChoices.DISLIKE


class FavoriteQuestionReactionFactory(QuestionReactionFactory):
    reaction = QuestionReaction.ReactionChoices.FAVORITE
