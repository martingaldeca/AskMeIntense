from logging import Logger
from unittest import mock

import freezegun
from core.factories import UserFactory
from core.models import User
from data.events import DataEvent
from django.test import TestCase


class BaseDataEventTestCase(TestCase):
    def setUp(self):
        self.user: User = UserFactory()
        self.event = DataEvent(
            user_identifier=self.user.uuid.hex,
            extra_info={"test_key": "test_value"},
            user_properties=self.user.properties_dict,
            app_version="app_version",
            device={"test_key": "test_value"},
            description="description",
            sender_agent="sender_agent",
        )
        self.event.sender_agent = "test_sender_agent"
        self.event.api_key = "test-key"

    def test_str(self):
        self.assertEqual(
            str(self.event),
            f"{self.event.event_type}-{self.event.user_identifier}-{self.event.app_version}",
        )

    @freezegun.freeze_time("1994-08-08")
    def test_data(self):
        self.assertEqual(
            self.event.data,
            {
                "timestamp": "1994-08-08T00:00:00+00:00",
                "event_type": self.event.event_type,
                "user_identifier": self.event.user_identifier,
                "extra_info": self.event.extra_info,
                "user_properties": self.event.user_properties,
                "app_version": self.event.app_version,
                "location": self.event.location,
                "device": self.event.device,
            },
        )

    def test_api_key(self):
        self.assertEqual(self.event.api_key, "test-key")

    @mock.patch("data.events.base.requests.post")
    @mock.patch.object(Logger, "warning")
    def test_send_ok(self, mock_logger_warning, mock_post):
        test_data_list = [
            (
                "not_received_with_error",
                {"event_received": False, "event_error": "test_error"},
                {"event_received": False, "event_error": "test_error"},
                1,
                "test_error",
            ),
            (
                "not_received_without_error",
                {"event_received": False},
                {"event_received": False},
                1,
                None,
            ),
            ("received", {"event_received": True}, {"event_received": True}, 0, None),
        ]
        for test_data in test_data_list:
            with self.subTest(msg=test_data[0]):
                (
                    _,
                    json_mocked_value,
                    expected_send_response,
                    logger_count,
                    extra_error,
                ) = test_data
                mock_response = mock.MagicMock()
                mock_response.json.return_value = json_mocked_value
                mock_post.return_value = mock_response
                self.assertEqual(self.event.send(), expected_send_response)
                self.assertEqual(mock_logger_warning.call_count, logger_count)
                if logger_count:
                    self.assertEqual(
                        mock_logger_warning.call_args,
                        mock.call(
                            "Bad response sending event to data-events",
                            extra={"event": str(self.event), "error": extra_error},
                        ),
                    )
            mock_logger_warning.reset_mock()

    @mock.patch("data.events.base.requests.post")
    @mock.patch.object(Logger, "error")
    def test_send_raise_error(self, mock_logger_error, mock_post):
        mock_post.side_effect = Exception("test_exception")
        with self.assertRaisesMessage(Exception, "test_exception"):
            self.event.send()
        self.assertEqual(mock_logger_error.call_count, 1)
        self.assertEqual(
            mock_logger_error.call_args,
            mock.call(
                "Problem sending event to data-events",
                extra={"event": str(self.event), "exception": "test_exception"},
            ),
        )
