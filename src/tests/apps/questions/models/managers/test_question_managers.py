from django.test import TestCase
from questions.factories import (
    ApprovedQuestionFactory,
    DeniedQuestionFactory,
    QuestionFactory,
)
from questions.models import Question


class QuestionManagersTestCase(TestCase):
    def test_approved(self):
        approved_question = ApprovedQuestionFactory()
        DeniedQuestionFactory()
        QuestionFactory()

        self.assertEqual(Question.objects.count(), 3)
        self.assertEqual(Question.objects.approved.count(), 1)
        self.assertEqual(Question.objects.approved.last(), approved_question)

    def test_denied(self):
        ApprovedQuestionFactory()
        denied_question = DeniedQuestionFactory()
        QuestionFactory()

        self.assertEqual(Question.objects.count(), 3)
        self.assertEqual(Question.objects.denied.count(), 1)
        self.assertEqual(Question.objects.denied.last(), denied_question)

    def test_pending_review(self):
        ApprovedQuestionFactory()
        DeniedQuestionFactory()
        pending_question = QuestionFactory()

        self.assertEqual(Question.objects.count(), 3)
        self.assertEqual(Question.objects.pending_review.count(), 1)
        self.assertEqual(Question.objects.pending_review.last(), pending_question)
