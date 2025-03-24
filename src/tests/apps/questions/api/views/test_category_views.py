from core.api.api_test_helpers import APITestBase
from django.urls import reverse
from questions.api.serializers import CategorySerializer
from questions.factories import CategoryFactory
from questions.models import Category
from rest_framework import status


class CategoryListViewTestCase(APITestBase):
    url = reverse("questions:categories")

    def setUp(self):
        super().setUp()
        self.category: Category = CategoryFactory()

    def test_get_categories_list_200_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            CategorySerializer(
                instance=[self.category], many=True, context={"request": self.request}
            ).data,
        )
        self.assertEqual(response.data["count"], 1)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
