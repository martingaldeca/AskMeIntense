from django.test import TestCase
from questions.factories import (
    DislikedQuestionReactionFactory,
    FavoriteQuestionReactionFactory,
    LikedQuestionReactionFactory,
)
from questions.models import QuestionReaction


class QuestionReactionManagersTestCase(TestCase):
    def test_liked(self):
        liked_question = LikedQuestionReactionFactory()
        DislikedQuestionReactionFactory()
        FavoriteQuestionReactionFactory()

        self.assertEqual(QuestionReaction.objects.count(), 3)
        self.assertEqual(QuestionReaction.objects.liked.count(), 1)
        self.assertEqual(QuestionReaction.objects.liked.last(), liked_question)

    def test_disliked(self):
        LikedQuestionReactionFactory()
        disliked_question = DislikedQuestionReactionFactory()
        FavoriteQuestionReactionFactory()

        self.assertEqual(QuestionReaction.objects.count(), 3)
        self.assertEqual(QuestionReaction.objects.disliked.count(), 1)
        self.assertEqual(QuestionReaction.objects.disliked.last(), disliked_question)

    def test_favorites(self):
        LikedQuestionReactionFactory()
        DislikedQuestionReactionFactory()
        pending_question = FavoriteQuestionReactionFactory()

        self.assertEqual(QuestionReaction.objects.count(), 3)
        self.assertEqual(QuestionReaction.objects.favorite.count(), 1)
        self.assertEqual(QuestionReaction.objects.favorite.last(), pending_question)
