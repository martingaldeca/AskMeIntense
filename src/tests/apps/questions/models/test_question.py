from django.db import IntegrityError
from django.test import TestCase
from questions.exceptions import NotValidQuestionStatusForApproveOrDeny
from questions.factories import (
    ApprovedQuestionFactory,
    CategoryFactory,
    DeniedQuestionFactory,
    LevelFactory,
    QuestionFactory,
)
from questions.models import Category, Level, Question


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
            with self.subTest(factory_to_use=factory_to_use), self.assertRaises(NotValidQuestionStatusForApproveOrDeny):
                question = factory_to_use()
                question.approve()

    def test_deny_not_valid_status(self):
        factories_to_use = [ApprovedQuestionFactory, DeniedQuestionFactory]
        for factory_to_use in factories_to_use:
            with self.subTest(factory_to_use=factory_to_use), self.assertRaises(NotValidQuestionStatusForApproveOrDeny):
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
