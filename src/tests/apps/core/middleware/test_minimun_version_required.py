from core.api.api_test_helpers import APITestBase
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from waffle.testutils import override_switch


class MinimumVersionRequiredTestCase(APITestBase):
    url = reverse("core:me")

    @override_switch("minimum_version_required_active", True)
    @override_settings(MINIMUM_REQUIRED_APP_VERSION_ANDROID="2.0.0")
    def test_version_not_valid(self):

        response = self.client.get(self.url, HTTP_APPVERSION="1.0.0")
        self.assertEqual(response.status_code, status.HTTP_426_UPGRADE_REQUIRED)
        self.assertEqual({"upgrade": "2.0.0"}, response.json())

    @override_switch("minimum_version_required_active", True)
    @override_settings(MINIMUM_REQUIRED_APP_VERSION_ANDROID="1.0.0")
    def test_version_valid(self):
        response = self.client.get(self.url, HTTP_APPVERSION="2.0.0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_switch("minimum_version_required_active", True)
    def test_version_not_valid_format(self):
        response = self.client.get(self.url, HTTP_APPVERSION="not_valid_format")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            {"error": "Invalid version: 'not_valid_format'"}, response.json()
        )
