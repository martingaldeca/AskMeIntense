from core.helpers import UUIDModelSerializerMixin
from questions.models import Category


class CategorySerializer(UUIDModelSerializerMixin):
    class Meta:
        model = Category
        fields = ["uuid", "name", "description", "icon"]
