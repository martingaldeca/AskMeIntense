from core.factories import UserFactory
from core.models import User
from django.db import IntegrityError
from django.test import TestCase
from questions.exceptions import NotValidQuestionStatusForApproveOrDeny
from questions.factories import (
    ApprovedQuestionFactory,
    CategoryFactory,
    DeniedQuestionFactory,
    DislikedQuestionFactory,
    FavoriteQuestionFactory,
    LevelFactory,
    LikedQuestionFactory,
    QuestionFactory,
)
from questions.models import Category, Level, Question, QuestionReaction


class QuestionTestCase(TestCase):
    def test_approve(self):
        question: Question = QuestionFactory()
        self.assertEqual(question.status, Question.StatusChoices.STATUS_PENDING_REVIEW)
        question.approve()
        self.assertEqual(question.status, Question.StatusChoices.STATUS_APPROVED)

    def test_deny(self):
        question: Question = QuestionFactory()
        self.assertEqual(question.status, Question.StatusChoices.STATUS_PENDING_REVIEW)
        question.deny()
        self.assertEqual(question.status, Question.StatusChoices.STATUS_DENIED)

    def test_approve_not_valid_status(self):
        factories_to_use = [ApprovedQuestionFactory, DeniedQuestionFactory]
        for factory_to_use in factories_to_use:
            with self.subTest(factory_to_use=factory_to_use), self.assertRaises(
                NotValidQuestionStatusForApproveOrDeny
            ):
                question = factory_to_use()
                question.approve()

    def test_deny_not_valid_status(self):
        factories_to_use = [ApprovedQuestionFactory, DeniedQuestionFactory]
        for factory_to_use in factories_to_use:
            with self.subTest(factory_to_use=factory_to_use), self.assertRaises(
                NotValidQuestionStatusForApproveOrDeny
            ):
                question = factory_to_use()
                question.deny()

    def test_add_level_category(self):
        question: Question = QuestionFactory(add_level_categories__total=0)
        new_category: Category = CategoryFactory()
        new_level: Level = LevelFactory()
        self.assertFalse(question.categories.filter(id=new_category.id).exists())
        self.assertFalse(question.levels.filter(id=new_level.id).exists())
        question.add_level_category(level=new_level, category=new_category)
        self.assertTrue(question.categories.filter(id=new_category.id).exists())
        self.assertTrue(question.levels.filter(id=new_level.id).exists())

    def test_can_not_add_repeated_level_category(self):
        question: Question = QuestionFactory(add_level_categories__total=1)
        category = question.categories.first()
        level = question.levels.first()
        with self.assertRaises(IntegrityError):
            question.add_level_category(level=level, category=category)

    def test_react(self):
        question: Question = ApprovedQuestionFactory()
        user: User = UserFactory()
        self.assertFalse(user.is_liked_question(question))
        question._react(QuestionReaction.ReactionChoices.LIKE, user)
        self.assertTrue(user.is_liked_question(question))

    def test_react_not_valid_reaction(self):
        question: Question = ApprovedQuestionFactory()
        user: User = UserFactory()
        self.assertFalse(user.is_liked_question(question))
        with self.assertRaises(ValueError) as expected_error:
            question._react("not_valid_reaction", user)
        self.assertEqual(expected_error.exception.args[0], "Reaction not valid")

    def test_react_like(self):
        user: User = UserFactory()
        question: Question = DislikedQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_disliked_question(question))
        question.react_like(user)
        self.assertFalse(user.is_disliked_question(question))
        self.assertTrue(user.is_liked_question(question))

    def test_react_dislike(self):
        user: User = UserFactory()
        question: Question = LikedQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_liked_question(question))
        question.react_dislike(user)
        self.assertFalse(user.is_liked_question(question))
        self.assertTrue(user.is_disliked_question(question))

    def test_react_favorite(self):
        question: Question = ApprovedQuestionFactory()
        user: User = UserFactory()
        question.react_favorite(user)
        self.assertTrue(user.is_favorite_question(question))

    def test_remove_reaction(self):
        user: User = UserFactory()
        question: Question = DislikedQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_disliked_question(question))
        question._remove_reaction(QuestionReaction.ReactionChoices.DISLIKE, user)
        self.assertFalse(user.is_disliked_question(question))

    def test_remove_reaction_not_valid(self):
        question: Question = ApprovedQuestionFactory()
        user: User = UserFactory()
        with self.assertRaises(ValueError) as expected_error:
            question._remove_reaction("not_valid_reaction", user)
        self.assertEqual(expected_error.exception.args[0], "Reaction not valid")

    def test_remove_like(self):
        user: User = UserFactory()
        question: Question = LikedQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_liked_question(question))
        question.remove_like(user)
        self.assertFalse(user.is_liked_question(question))

    def test_remove_dislike(self):
        user: User = UserFactory()
        question: Question = DislikedQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_disliked_question(question))
        question.remove_dislike(user)
        self.assertFalse(user.is_disliked_question(question))

    def test_remove_favorite(self):
        user: User = UserFactory()
        question: Question = FavoriteQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_favorite_question(question))
        question.remove_favorite(user)
        self.assertFalse(user.is_favorite_question(question))

    def test_not_possible_like_twice(self):
        user: User = UserFactory()
        question: Question = LikedQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_liked_question(question))
        with self.assertRaises(IntegrityError):
            question.react_like(user)

    def test_not_possible_dislike_twice(self):
        user: User = UserFactory()
        question: Question = DislikedQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_disliked_question(question))
        with self.assertRaises(IntegrityError):
            question.react_dislike(user)

    def test_not_possible_favorite_twice(self):
        user: User = UserFactory()
        question: Question = FavoriteQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_favorite_question(question))
        with self.assertRaises(IntegrityError):
            question.react_favorite(user)
