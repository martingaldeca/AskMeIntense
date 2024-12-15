from core.api.api_test_helpers import APITestBase
from django.urls import reverse
from questions.api.serializers import LevelSerializer
from questions.factories import LevelFactory
from questions.models import Level
from rest_framework import status


class LevelListViewTestCase(APITestBase):
    url = reverse("questions:levels")

    def setUp(self):
        super().setUp()
        self.level: Level = LevelFactory()

    def test_get_levels_list_200_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            LevelSerializer(
                instance=[
                    self.level,
                ],
                many=True,
                context={"request": self.request},
            ).data,
        )
        self.assertEqual(response.data["count"], 1)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

    def test_get_me_detail_not_logged_401_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"].code, "not_authenticated")
