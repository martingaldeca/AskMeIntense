import uuid

from core.api.api_test_helpers import APITestBase
from django.urls import reverse
from questions.api.serializers import QuestionSerializer, SimpleQuestionSerializer
from questions.factories import ApprovedQuestionFactory
from questions.models import Question
from rest_framework import status


class QuestionListViewTestCase(APITestBase):
    url = reverse("questions:questions")

    def setUp(self):
        super().setUp()
        self.question: Question = ApprovedQuestionFactory()

    def test_get_questions_list_200_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            QuestionSerializer(
                instance=[
                    self.question,
                ],
                many=True,
                context={"request": self.request},
            ).data,
        )
        self.assertEqual(response.data["count"], 1)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

    def test_get_question_list_by_category_200_ok(self):
        test_data_list = [
            [self.question.categories.first().uuid.hex, 1],
            [uuid.uuid4().hex, 0],
        ]
        for test_data in test_data_list:
            category_uuid, total_count = test_data
            response = self.client.get(self.url, query_params={"category": category_uuid})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], total_count)

    def test_get_question_list_by_level_200_ok(self):
        test_data_list = [
            [self.question.levels.first().uuid.hex, 1],
            [uuid.uuid4().hex, 0],
        ]
        for test_data in test_data_list:
            level_uuid, total_count = test_data
            response = self.client.get(self.url, query_params={"level": level_uuid})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], total_count)


class RandomQuestionViewTestCase(APITestBase):
    url = reverse("questions:random_question", kwargs={"level": None, "category": None})

    def setUp(self):
        super().setUp()
        self.question_1: Question = ApprovedQuestionFactory(
            add_level_categories__level_number=1, add_level_categories__category_name="testing"
        )
        self.question_2: Question = ApprovedQuestionFactory(
            add_level_categories__level_number=1, add_level_categories__category_name="testing"
        )
        self.question_3: Question = ApprovedQuestionFactory(
            add_level_categories__level_number=1, add_level_categories__category_name="testing"
        )

    def test_get_random_question_200_ok(self):
        self.url = reverse(
            "questions:random_question",
            kwargs={
                "level": self.question_1.levels.first().uuid.hex,
                "category": self.question_1.categories.first().uuid.hex,
            },
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            response.data,
            [
                SimpleQuestionSerializer(
                    instance=instance,
                    context={"request": self.request},
                ).data
                for instance in [self.question_1, self.question_2, self.question_3]
            ],
        )
