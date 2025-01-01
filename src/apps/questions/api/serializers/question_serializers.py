from core.helpers import UUIDModelSerializerMixin
from questions.api.serializers import CategorySerializer, LevelSerializer
from questions.models import Question
from rest_framework import serializers


class SimpleQuestionSerializer(UUIDModelSerializerMixin):
    liked = serializers.SerializerMethodField("is_liked")
    disliked = serializers.SerializerMethodField("is_disliked")
    favorite = serializers.SerializerMethodField("is_favorite")

    class Meta:
        model = Question
        fields = ["uuid", "question", "status", "example", "liked", "disliked", "favorite"]

    def is_liked(self, obj: Question):
        if (request := self.context.get("request")) and (user := request.user) and not user.is_anonymous:
            return user.is_liked_question(obj)
        return False

    def is_disliked(self, obj: Question):
        if (request := self.context.get("request")) and (user := request.user) and not user.is_anonymous:
            return user.is_disliked_question(obj)
        return False

    def is_favorite(self, obj: Question):
        if (request := self.context.get("request")) and (user := request.user) and not user.is_anonymous:
            return user.is_favorite_question(obj)
        return False


class QuestionSerializer(SimpleQuestionSerializer):
    categories = CategorySerializer(many=True)
    levels = LevelSerializer(many=True)

    class Meta:
        model = Question
        fields = ["uuid", "question", "status", "example", "categories", "levels", "liked", "disliked", "favorite"]
