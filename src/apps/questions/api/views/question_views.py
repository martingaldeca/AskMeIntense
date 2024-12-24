from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema

from core.mixins import MultipleFieldLookupMixin
from questions.api.serializers import QuestionSerializer, SimpleQuestionSerializer
from questions.models import Question
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny


@extend_schema(
    tags=["questions"],
    parameters=[
        OpenApiParameter(name="category", description=_("Category uuid"), type=str),
        OpenApiParameter(name="level", description=_("Level uuid"), type=str),
    ],
)
class QuestionListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.approved.all()
        if category_uuid := self.request.query_params.get("category", None):
            queryset = queryset.filter(categories__uuid=category_uuid)

        if level_uuid := self.request.query_params.get("level", None):
            queryset = queryset.filter(levels__uuid=level_uuid)

        return queryset


@extend_schema(tags=["questions"])
class RandomQuestionGetView(MultipleFieldLookupMixin, RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SimpleQuestionSerializer
    queryset = Question.objects.approved.all()
    lookup_fields = ["categories__uuid", "levels__uuid"]
    lookup_url_kwargs = ["category", "level"]
    random_result_from_list = True
