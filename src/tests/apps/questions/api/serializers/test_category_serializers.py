from core.api.api_test_helpers import SerializerTestBase
from questions.api.serializers import CategorySerializer
from questions.factories import CategoryFactory
from questions.models import Category


class CategorySerializerTestCase(SerializerTestBase):
    def test_data(self):
        category: Category = CategoryFactory()
        expected_data = {
            "uuid": category.uuid.hex,
            "name": category.name,
            "description": category.description,
            "icon": self.request.build_absolute_uri(category.icon.url),
        }
        self.assertEqual(CategorySerializer(category, context=self.context).data, expected_data)
