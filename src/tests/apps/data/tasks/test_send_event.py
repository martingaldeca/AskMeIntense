from unittest import mock
from unittest.mock import MagicMock

from core.factories import UserFactory
from core.models import User
from data.events import DataEvent
from data.tasks.send_event import rsync_user_properties, send_event
from django.test import TestCase


class SendEventTaskTestCase(TestCase):
    def setUp(self):
        self.user: User = UserFactory()
        self.event_type = DataEvent.event_type
        self.user_identifier = self.user.uuid.hex
        self.extra_info = {"test_key": "test_value"}
        self.user_properties = {"test_key": "test_value"}
        self.request_headers = {"_store": {"appversion": ("ignored", "Test-0.0.0")}}
        self.app_version = "0.0.0"
        self.device = {"test_key": "test_value"}

        self.event_arguments = {
            "event_type": self.event_type,
            "user_identifier": self.user_identifier,
            "extra_info": self.extra_info,
            "user_properties": self.user_properties,
            "request_headers": self.request_headers,
            "app_version": self.app_version,
            "device": self.device,
        }

    @mock.patch.object(DataEvent, "send")
    def test_send_event(self, mock_send_event):
        event = send_event(
            **self.event_arguments,
        )
        self.assertEqual(mock_send_event.call_count, 1)
        self.assertEqual(event.user_identifier, self.user_identifier)
        self.assertEqual(event.extra_info, self.extra_info)
        self.assertEqual(
            event.user_properties, {**self.user.properties_dict, **self.user_properties}
        )
        self.assertEqual(event.app_version, "Test-0.0.0")
        self.assertEqual(event.device, self.device)
        self.assertEqual(event.description, DataEvent.description)
        self.assertIsNone(event.sender_agent)

    @mock.patch.object(DataEvent, "send")
    def test_send_without_app_version_event(self, mock_send_event):
        event_arguments_without_app_version = self.event_arguments.copy()
        event_arguments_without_app_version["request_headers"] = None
        event = send_event(
            **event_arguments_without_app_version,
        )
        self.assertEqual(mock_send_event.call_count, 1)
        self.assertEqual(event.user_identifier, self.user_identifier)
        self.assertEqual(event.extra_info, self.extra_info)
        self.assertEqual(
            event.user_properties, {**self.user.properties_dict, **self.user_properties}
        )
        self.assertEqual(event.app_version, "0.0.0")
        self.assertEqual(event.device, self.device)
        self.assertEqual(event.description, DataEvent.description)
        self.assertIsNone(event.sender_agent)

    @mock.patch.object(DataEvent, "send")
    def test_send_without_user_identifier_event(self, mock_send_event):
        event_arguments_without_app_version = self.event_arguments.copy()
        event_arguments_without_app_version["user_identifier"] = None
        event = send_event(
            **event_arguments_without_app_version,
        )
        self.assertEqual(mock_send_event.call_count, 1)
        self.assertIsNone(event.user_identifier)
        self.assertEqual(event.extra_info, self.extra_info)
        self.assertEqual(event.user_properties, {**self.user_properties})
        self.assertEqual(event.app_version, "Test-0.0.0")
        self.assertEqual(event.device, self.device)
        self.assertEqual(event.description, DataEvent.description)
        self.assertIsNone(event.sender_agent)


class RSyncUserPropertiesTaskTestCase(TestCase):
    def test_rsync_user_properties(self):
        user1 = UserFactory()
        user2 = UserFactory()
        dummy_event_instance = MagicMock()
        dummy_event_callable = MagicMock(return_value=dummy_event_instance)
        with mock.patch.dict(
            "data.tasks.send_event.events",
            {"rsync_user_properties_event": dummy_event_callable},
        ):
            rsync_user_properties()
            self.assertEqual(dummy_event_callable.call_count, 2)
            calls = dummy_event_callable.call_args_list
            expected_calls = [
                {
                    "user_identifier": user1.uuid.hex,
                    "user_properties": user1.properties_dict,
                },
                {
                    "user_identifier": user2.uuid.hex,
                    "user_properties": user2.properties_dict,
                },
            ]
            for call, expected in zip(calls, expected_calls):
                args, kwargs = call
                self.assertEqual(kwargs, expected)
            self.assertEqual(dummy_event_instance.send.call_count, 2)
