from drf_spectacular.utils import extend_schema
from questions.api.serializers import LevelSerializer
from questions.models import Level
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


@extend_schema(
    tags=["questions"],
)
class LevelListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Level.objects.all().order_by("number")
    serializer_class = LevelSerializer
