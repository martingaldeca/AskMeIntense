from core.api.api_test_helpers import SerializerTestBase
from questions.api.serializers import CategorySerializer, LevelSerializer, QuestionSerializer
from questions.factories import QuestionFactory
from questions.models import Question


class QuestionSerializerTestCase(SerializerTestBase):
    def test_data(self):
        question: Question = QuestionFactory()
        expected_data = {
            "uuid": question.uuid.hex,
            "question": question.question,
            "status": question.status,
            "example": question.example,
            "categories": CategorySerializer(question.categories.all(), many=True).data,
            "levels": LevelSerializer(question.levels.all(), many=True).data,
        }
        self.assertEqual(QuestionSerializer(question).data, expected_data)
