from unittest import mock
from unittest.mock import patch

from core.api.api_test_helpers import APITestBase
from data.api.views import DataEventView
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from rest_framework import status


class DataEventViewTestCase(APITestBase):
    url = reverse("data:data-event")

    def setUp(self):
        super().setUp()
        self.event_posted = {
            "event_type": "test_event",
            "app_version": "Test-0.0.0",
            "extra_info": {"test_key": "test_value"},
        }

    @patch("data.api.views.data_event_views.send_event")
    @patch.object(DataEventView, "serializer_class")
    def test_post_event_logged_201_ok(self, event_serializer_mocked, send_event_mocked):
        event_serializer_mocked().validated_data = self.event_posted
        response = self.client.post(self.url, self.event_posted, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(event_serializer_mocked.call_count, 2)
        self.assertEqual(event_serializer_mocked().is_valid.call_count, 1)
        self.assertEqual(
            event_serializer_mocked().is_valid.call_args,
            mock.call(raise_exception=True, user=self.user),
        )
        self.assertEqual(event_serializer_mocked().device_parser.call_count, 1)
        self.assertEqual(send_event_mocked.delay.call_count, 1)
        self.assertEqual(
            send_event_mocked.delay.call_args, mock.call(**self.event_posted)
        )

    @patch("data.api.views.data_event_views.send_event")
    @patch.object(DataEventView, "serializer_class")
    def test_post_event_not_logged_201_ok(
        self, event_serializer_mocked, send_event_mocked
    ):
        event_serializer_mocked().validated_data = self.event_posted
        self.client.logout()
        response = self.client.post(self.url, self.event_posted, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(event_serializer_mocked.call_count, 2)
        self.assertEqual(event_serializer_mocked().is_valid.call_count, 1)
        self.assertEqual(
            event_serializer_mocked().is_valid.call_args,
            mock.call(raise_exception=True, user=AnonymousUser()),
        )
        self.assertEqual(event_serializer_mocked().device_parser.call_count, 1)
        self.assertEqual(send_event_mocked.delay.call_count, 1)
        self.assertEqual(
            send_event_mocked.delay.call_args, mock.call(**self.event_posted)
        )
