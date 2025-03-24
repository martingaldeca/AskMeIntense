from core.mixins import MultipleFieldLookupMixin
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema
from questions.api.serializers import (
    AddOrRemoveInputReactionRequestSerializer,
    AddOrRemoveReactionSerializer,
    QuestionSerializer,
    SimpleQuestionSerializer,
)
from questions.models import Question, QuestionReaction
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny, IsAuthenticated


@extend_schema(
    tags=["questions"],
    parameters=[
        OpenApiParameter(name="category", description=_("Category uuid"), type=str),
        OpenApiParameter(name="level", description=_("Level uuid"), type=str),
    ],
)
class QuestionListView(ListAPIView):
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
    serializer_class = SimpleQuestionSerializer
    queryset = Question.objects.approved.all()
    lookup_fields = ["categories__uuid", "levels__uuid"]
    lookup_url_kwargs = ["category", "level"]
    random_result_from_list = True


@extend_schema(
    tags=["questions"],
    parameters=[
        OpenApiParameter(name="category", description=_("Category uuid"), type=str),
        OpenApiParameter(name="level", description=_("Level uuid"), type=str),
    ],
)
class FavoriteQuestionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = self.request.user.favorite_questions.order_by("levels__number")

        if category_uuid := self.request.query_params.get("category", None):
            queryset = queryset.filter(categories__uuid=category_uuid)

        if level_uuid := self.request.query_params.get("level", None):
            queryset = queryset.filter(levels__uuid=level_uuid)

        return queryset


@extend_schema(
    request=AddOrRemoveInputReactionRequestSerializer,
    responses=AddOrRemoveReactionSerializer,
)
class ReactToQuestionView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddOrRemoveReactionSerializer

    def perform_create(self, serializer):
        serializer.instance = get_object_or_404(Question, uuid=self.kwargs["uuid"])
        reaction = serializer.validated_data["reaction"]
        user = self.request.user

        if reaction == QuestionReaction.ReactionChoices.LIKE:
            serializer.instance.react_like(user)
        elif reaction == QuestionReaction.ReactionChoices.DISLIKE:
            serializer.instance.react_dislike(user)
        else:  # reaction == QuestionReaction.ReactionChoices.FAVORITE:
            serializer.instance.react_favorite(user)


@extend_schema(
    request=AddOrRemoveInputReactionRequestSerializer,
    responses=AddOrRemoveReactionSerializer,
)
class RemoveReactionView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddOrRemoveReactionSerializer

    def perform_create(self, serializer):
        serializer.instance = get_object_or_404(Question, uuid=self.kwargs["uuid"])
        reaction = serializer.validated_data["reaction"]
        user = self.request.user

        if reaction == QuestionReaction.ReactionChoices.LIKE:
            serializer.instance.remove_like(user)
        elif reaction == QuestionReaction.ReactionChoices.DISLIKE:
            serializer.instance.remove_dislike(user)
        else:  # reaction == QuestionReaction.ReactionChoices.FAVORITE:
            serializer.instance.remove_favorite(user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_202_ACCEPTED
        return response
