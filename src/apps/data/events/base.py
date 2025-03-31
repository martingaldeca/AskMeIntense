import logging
import os
from functools import cached_property

import requests
from django.utils import timezone

env = os.environ
logger = logging.getLogger(__name__)


class DataEvent:
    SENDER_AGENT_FRONTEND, SENDER_AGENT_BACKEND = "frontend", "backend"

    url = f"{env.get('DATA_EVENTS_URL')}/event"
    api_key = env.get("DATA_EVENTS_API_KEY")
    event_type = "test_event"
    user_identifier = None
    extra_info = None
    user_properties = None
    app_version = None
    location = None
    device = None

    description = None
    sender_agent = None

    def __init__(
        self,
        user_identifier: str = None,
        extra_info: dict = None,
        user_properties: str = None,
        app_version: str = None,
        location: dict = None,
        device: dict = None,
        description: str = None,
        sender_agent: str = None,
    ):
        self.user_identifier = user_identifier
        self.extra_info = extra_info
        self.user_properties = user_properties
        self.app_version = app_version
        self.location = location
        self.device = device
        if description:
            self.description = description
        if sender_agent:
            self.sender_agent = sender_agent

    def __str__(self):
        return f"{self.event_type}-{self.user_identifier}-{self.app_version}"

    @property
    def data(self):
        self.extra_info["sender_agent"] = self.sender_agent
        return {
            "timestamp": timezone.now().isoformat(),
            "event_type": self.event_type,
            "user_identifier": self.user_identifier,
            "extra_info": self.extra_info,
            "user_properties": self.user_properties,
            "app_version": self.app_version,
            "location": self.location,
            "device": self.device,
        }

    @cached_property
    def headers(self):
        return {"Authorization": "Bearer " + self.api_key}

    def send(self):
        try:
            logger.info(self.data)
            response = requests.post(self.url, json=self.data, headers=self.headers)
        except Exception as ex:
            logger.error(
                "Problem sending event to data-events",
                extra={"event": str(self), "exception": ex},
            )
            raise ex

        if not response.json().get("event_received", False) or response.json().get(
            "event_error", False
        ):
            logger.info(response.json())
            logger.warning(
                "Bad response sending event to data-events",
                extra={
                    "event": str(self),
                    "error": response.json().get("event_error", None),
                },
            )


class BackendDataEvent(DataEvent):
    sender_agent = DataEvent.SENDER_AGENT_BACKEND


class FrontendDataEvent(DataEvent):
    sender_agent = DataEvent.SENDER_AGENT_FRONTEND


class RsyncUserPropertiesEvent(BackendDataEvent):
    event_type = "rsync_user_properties_event"
    description = "This event is used to rsync the user properties."
