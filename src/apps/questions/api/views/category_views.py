from drf_spectacular.utils import extend_schema
from questions.api.serializers import CategorySerializer
from questions.models import Category
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


@extend_schema(
    tags=["questions"],
)
class CategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
