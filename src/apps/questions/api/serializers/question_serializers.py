from core.helpers import UUIDModelSerializerMixin
from django.utils.translation import gettext_lazy as _
from questions.api.serializers import CategorySerializer, LevelSerializer
from questions.models import Question
from rest_framework import serializers


class SimpleQuestionSerializer(UUIDModelSerializerMixin):
    liked = serializers.SerializerMethodField(help_text=_("Field that indicate if the question is liked by the user."))
    disliked = serializers.SerializerMethodField(
        help_text=_("Field that indicate if the question is disliked by the user.")
    )
    favorite = serializers.SerializerMethodField(
        help_text=_("Field that indicate if the question is one of the user's favorite questions.")
    )

    class Meta:
        model = Question
        fields = ["uuid", "question", "status", "example", "liked", "disliked", "favorite"]

    def get_liked(self, obj: Question) -> bool:
        if (request := self.context.get("request")) and (user := request.user) and not user.is_anonymous:
            return user.is_liked_question(obj)
        return False

    def get_disliked(self, obj: Question) -> bool:
        if (request := self.context.get("request")) and (user := request.user) and not user.is_anonymous:
            return user.is_disliked_question(obj)
        return False

    def get_favorite(self, obj: Question) -> bool:
        if (request := self.context.get("request")) and (user := request.user) and not user.is_anonymous:
            return user.is_favorite_question(obj)
        return False


class QuestionSerializer(SimpleQuestionSerializer):
    categories = CategorySerializer(many=True, help_text=_("Categories of the question"))
    levels = LevelSerializer(many=True, help_text=_("Levels of the question"))

    class Meta:
        model = Question
        fields = ["uuid", "question", "status", "example", "categories", "levels", "liked", "disliked", "favorite"]
