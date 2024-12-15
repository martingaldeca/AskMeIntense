from core.helpers import UUIDModelSerializerMixin
from questions.api.serializers import CategorySerializer, LevelSerializer
from questions.models import Question


class QuestionSerializer(UUIDModelSerializerMixin):
    categories = CategorySerializer(many=True)
    levels = LevelSerializer(many=True)

    class Meta:
        model = Question
        fields = ["uuid", "question", "status", "example", "categories", "levels"]
