from drf_spectacular.utils import extend_schema
from questions.api.serializers import CategorySerializer
from questions.models import Category
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["questions"],
)
class CategoryListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
