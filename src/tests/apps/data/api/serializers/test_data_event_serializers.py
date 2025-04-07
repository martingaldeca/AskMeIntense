from unittest.mock import patch

from core.factories import UserFactory
from data.api.serializers import DataEventSerializer
from data.events import events
from data.exceptions import NotValidEventException
from django.test import TestCase


class DataEventSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_event_type = "test_event"
        self.events_patcher = patch.dict(
            events, {self.valid_event_type: True}, clear=True
        )
        self.events_patcher.start()

    def tearDown(self):
        self.events_patcher.stop()

    def test_valid_data_without_user(self):
        data = {
            "event_type": self.valid_event_type,
            "app_version": "1.0",
            "extra_info": {"key": "value"},
        }
        serializer = DataEventSerializer(data=data)
        valid = serializer.is_valid(raise_exception=True)
        self.assertTrue(valid)
        self.assertNotIn("user_identifier", serializer.validated_data)

    def test_valid_data_with_user(self):
        data = {
            "event_type": self.valid_event_type,
            "app_version": "1.0",
        }
        serializer = DataEventSerializer(data=data)
        user = UserFactory()  # Using UserFactory instead of a dummy user.
        valid = serializer.is_valid(raise_exception=True, user=user)
        self.assertTrue(valid)
        self.assertEqual(serializer.validated_data["user_identifier"], user.uuid.hex)

    def test_invalid_event_type(self):
        invalid_event = "invalid_event"
        data = {
            "event_type": invalid_event,
            "app_version": "1.0",
        }
        serializer = DataEventSerializer(data=data)
        with self.assertRaises(NotValidEventException) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(
            context.exception.args[0], f"Event type '{invalid_event}' is not valid"
        )

    @patch("data.api.serializers.data_event_serializers.parse")
    def test_device_parser(self, mock_parse):
        class DummyOS:
            def __init__(self):
                self.family = "DummyOS"
                self.version_string = "1.0"

        class DummyDevice:
            def __init__(self):
                self.family = "DummyDeviceFamily"
                self.brand = "DummyBrand"
                self.model = "DummyModel"

        class DummyUserAgent:
            def __init__(self):
                self.os = DummyOS()
                self.device = DummyDevice()
                self.is_bot = False
                self.is_pc = True
                self.is_touch_capable = False
                self.is_tablet = False
                self.is_mobile = False

        dummy_user_agent = DummyUserAgent()
        mock_parse.return_value = dummy_user_agent

        # Create a dummy request with necessary META attributes.
        class DummyRequest:
            META = {
                "HTTP_USER_AGENT": "dummy agent",
                "REMOTE_ADDR": "127.0.0.1",
                "DEFAULT_LOCALE": "en-US",
                "PRODUCTION": "True",
                "HTTP_SEC_CH_UA_PLATFORM": "Windows",
                "HTTP_SEC_CH_UA": "dummy browser",
                "HTTP_ORIGIN": "http://example.com",
                "HTTP_REFERER": "http://example.com/ref",
                "HTTP_ACCEPT_LANGUAGE": "en",
            }

        data = {
            "event_type": self.valid_event_type,
            "app_version": "1.0",
        }
        serializer = DataEventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.device_parser(DummyRequest())

        expected_device = {
            "ip": "127.0.0.1",
            "locale": "en-US",
            "production": "True",
            "platform": "Windows",
            "user_agent": "dummy agent",
            "browser": "dummy browser",
            "origin": "http://example.com",
            "referer": "http://example.com/ref",
            "language": "en",
            "user_agent_os_family": "DummyOS",
            "user_agent_os_version": "1.0",
            "user_agent_device_family": "DummyDeviceFamily",
            "user_agent_device_brand": "DummyBrand",
            "user_agent_device_model": "DummyModel",
            "user_agent_is_bot": False,
            "user_agent_is_pc": True,
            "user_agent_is_touch_capable": False,
            "user_agent_is_tablet": False,
            "user_agent_is_mobile": False,
        }
        self.assertEqual(serializer.validated_data["device"], expected_device)
