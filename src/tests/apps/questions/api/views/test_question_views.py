import uuid

from core.api.api_test_helpers import APITestBase, APITestBaseNeedAuthorized
from django.urls import reverse
from questions.api.serializers import QuestionSerializer, SimpleQuestionSerializer
from questions.factories import (
    ApprovedQuestionFactory,
    DislikedQuestionFactory,
    FavoriteQuestionFactory,
    LikedQuestionFactory,
)
from questions.models import Question, QuestionReaction
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


class FavoriteQuestionListViewTestCase(APITestBaseNeedAuthorized):
    url = reverse("questions:favorite_questions")

    def setUp(self):
        super().setUp()
        self.question: Question = FavoriteQuestionFactory(add_reaction__user=self.user)
        self.not_favorite_question: Question = ApprovedQuestionFactory()

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


class RandomQuestionViewTestCase(APITestBase):
    url = reverse("questions:random_question", kwargs={"level": None, "category": None})

    def setUp(self):
        super().setUp()
        self.question_1: Question = ApprovedQuestionFactory(
            add_level_categories__level_number=1,
            add_level_categories__category_name="testing",
        )
        self.question_2: Question = ApprovedQuestionFactory(
            add_level_categories__level_number=1,
            add_level_categories__category_name="testing",
        )
        self.question_3: Question = ApprovedQuestionFactory(
            add_level_categories__level_number=1,
            add_level_categories__category_name="testing",
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


class ReactToQuestionViewTestCase(APITestBaseNeedAuthorized):
    url = reverse("questions:question_react", kwargs={"uuid": None})

    def test_question_react_like_201_created(self):
        question: Question = ApprovedQuestionFactory()
        self.assertFalse(self.user.is_liked_question(question))
        self.url = reverse("questions:question_react", kwargs={"uuid": question.uuid.hex})
        response = self.client.post(self.url, data={"reaction": QuestionReaction.ReactionChoices.LIKE})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user.is_liked_question(question))

    def test_question_react_dislike_201_created(self):
        question: Question = ApprovedQuestionFactory()
        self.assertFalse(self.user.is_disliked_question(question))
        self.url = reverse("questions:question_react", kwargs={"uuid": question.uuid.hex})
        response = self.client.post(self.url, data={"reaction": QuestionReaction.ReactionChoices.DISLIKE})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user.is_disliked_question(question))

    def test_question_react_favorite_201_created(self):
        question: Question = ApprovedQuestionFactory()
        self.assertFalse(self.user.is_favorite_question(question))
        self.url = reverse("questions:question_react", kwargs={"uuid": question.uuid.hex})
        response = self.client.post(self.url, data={"reaction": QuestionReaction.ReactionChoices.FAVORITE})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user.is_favorite_question(question))

    def test_question_react_invalid_reaction_400_bad_request(self):
        question: Question = ApprovedQuestionFactory()
        self.assertFalse(self.user.is_liked_question(question))
        self.url = reverse("questions:question_react", kwargs={"uuid": question.uuid.hex})
        response = self.client.post(self.url, data={"reaction": "not_valid_reaction"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"reaction": ['"not_valid_reaction" no es una elección válida.']},
        )

    def test_question_react_like_remove_unlike_201_created(self):
        question: Question = DislikedQuestionFactory(add_reaction__user=self.user)
        self.assertTrue(self.user.is_disliked_question(question))
        self.assertFalse(self.user.is_liked_question(question))
        self.url = reverse("questions:question_react", kwargs={"uuid": question.uuid.hex})
        response = self.client.post(self.url, data={"reaction": QuestionReaction.ReactionChoices.LIKE})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(self.user.is_disliked_question(question))
        self.assertTrue(self.user.is_liked_question(question))

    def test_question_react_dislike_remove_like_201_created(self):
        question: Question = LikedQuestionFactory(add_reaction__user=self.user)
        self.assertTrue(self.user.is_liked_question(question))
        self.assertFalse(self.user.is_disliked_question(question))
        self.url = reverse("questions:question_react", kwargs={"uuid": question.uuid.hex})
        response = self.client.post(self.url, data={"reaction": QuestionReaction.ReactionChoices.DISLIKE})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(self.user.is_liked_question(question))
        self.assertTrue(self.user.is_disliked_question(question))


class RemoveReactionViewTestCase(APITestBaseNeedAuthorized):
    url = reverse("questions:question_remove_reaction", kwargs={"uuid": None})

    def test_question_remove_reaction_like_202_accepted(self):
        question: Question = LikedQuestionFactory(add_reaction__user=self.user)
        self.assertTrue(self.user.is_liked_question(question))
        self.url = reverse("questions:question_remove_reaction", kwargs={"uuid": question.uuid.hex})
        response = self.client.post(self.url, data={"reaction": QuestionReaction.ReactionChoices.LIKE})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(self.user.is_liked_question(question))

    def test_question_remove_reaction_dislike_202_accepted(self):
        question: Question = DislikedQuestionFactory(add_reaction__user=self.user)
        self.assertTrue(self.user.is_disliked_question(question))
        self.url = reverse("questions:question_remove_reaction", kwargs={"uuid": question.uuid.hex})
        response = self.client.post(self.url, data={"reaction": QuestionReaction.ReactionChoices.DISLIKE})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(self.user.is_disliked_question(question))

    def test_question_remove_reaction_favorite_202_accepted(self):
        question: Question = FavoriteQuestionFactory(add_reaction__user=self.user)
        self.assertTrue(self.user.is_favorite_question(question))
        self.url = reverse("questions:question_remove_reaction", kwargs={"uuid": question.uuid.hex})
        response = self.client.post(self.url, data={"reaction": QuestionReaction.ReactionChoices.FAVORITE})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(self.user.is_favorite_question(question))
