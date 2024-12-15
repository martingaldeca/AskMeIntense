from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema
from questions.api.serializers import QuestionSerializer
from questions.models import Question
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["questions"],
    parameters=[
        OpenApiParameter(name="category", description=_("Category uuid"), type=str),
        OpenApiParameter(name="level", description=_("Level uuid"), type=str),
    ],
)
class QuestionListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        if category_uuid := self.request.query_params.get("category", None):
            queryset = queryset.filter(categories__uuid=category_uuid)

        if level_uuid := self.request.query_params.get("level", None):
            queryset = queryset.filter(levels__uuid=level_uuid)

        return queryset
