from core.api.api_test_helpers import SerializerTestBase
from questions.api.serializers import (
    AddOrRemoveReactionSerializer,
    CategorySerializer,
    LevelSerializer,
    QuestionSerializer,
    SimpleQuestionSerializer,
)
from questions.factories import DislikedQuestionFactory, FavoriteQuestionFactory, LikedQuestionFactory, QuestionFactory
from questions.models import Question, QuestionReaction


class SimpleQuestionSerializerTestCase(SerializerTestBase):
    def test_data(self):
        question: Question = QuestionFactory()
        expected_data = {
            "uuid": question.uuid.hex,
            "question": question.question,
            "status": question.status,
            "example": question.example,
            "liked": False,
            "disliked": False,
            "favorite": False,
        }
        self.assertEqual(SimpleQuestionSerializer(question, context=self.context).data, expected_data)

    def test_liked_disliked_and_favorite(self):
        test_data_list = [
            [LikedQuestionFactory, True, False, False],
            [DislikedQuestionFactory, False, True, False],
            [FavoriteQuestionFactory, False, False, True],
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data):
                factory, liked, disliked, favorite = test_data
                question: Question = factory(add_reaction__user=self.user)
                expected_data = {
                    "uuid": question.uuid.hex,
                    "question": question.question,
                    "status": question.status,
                    "example": question.example,
                    "liked": liked,
                    "disliked": disliked,
                    "favorite": favorite,
                }
                self.assertEqual(SimpleQuestionSerializer(question, context=self.context).data, expected_data)


class QuestionSerializerTestCase(SerializerTestBase):
    def test_data(self):
        question: Question = QuestionFactory()
        expected_data = {
            "uuid": question.uuid.hex,
            "question": question.question,
            "status": question.status,
            "example": question.example,
            "categories": CategorySerializer(question.categories.all(), many=True, context=self.context).data,
            "levels": LevelSerializer(question.levels.all(), many=True, context=self.context).data,
            "liked": False,
            "disliked": False,
            "favorite": False,
        }
        self.assertEqual(QuestionSerializer(question, context=self.context).data, expected_data)


class AddOrRemoveReactionSerializerTestCase(SerializerTestBase):
    def test_data(self):
        question: Question = QuestionFactory()
        expected_data = {
            "uuid": question.uuid.hex,
            "question": question.question,
            "status": question.status,
            "example": question.example,
            "liked": False,
            "disliked": False,
            "favorite": False,
        }
        self.assertEqual(AddOrRemoveReactionSerializer(question, context=self.context).data, expected_data)

    def test_data_validation_valid(self):
        serializer = AddOrRemoveReactionSerializer(
            data={"reaction": QuestionReaction.ReactionChoices.LIKE}, context=self.context
        )
        self.assertTrue(serializer.is_valid())

    def test_data_validation_invalid(self):
        serializer = AddOrRemoveReactionSerializer(data={"reaction": "not_valid_reaction"}, context=self.context)
        self.assertFalse(serializer.is_valid())
