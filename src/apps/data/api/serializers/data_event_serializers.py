from data.events import events
from data.exceptions import NotValidEventException
from django.contrib.auth.models import User
from rest_framework import serializers
from user_agents import parse


class DataEventSerializer(serializers.Serializer):
    event_type = serializers.CharField(required=True)
    app_version = serializers.CharField(required=True)
    extra_info = serializers.JSONField(required=False)

    def is_valid(self, raise_exception=False, user: User = None):
        validation = super().is_valid(raise_exception=raise_exception)

        if (
            event_type := self.validated_data["event_type"]
        ) and event_type not in events.keys():
            raise NotValidEventException(event_type)
        if user and not user.is_anonymous:
            self.validated_data["user_identifier"] = user.uuid.hex
        return validation

    def device_parser(self, request):
        user_agent = parse(request.META.get("HTTP_USER_AGENT"))
        self.validated_data["device"] = {
            "ip": request.META.get("REMOTE_ADDR"),
            "locale": request.META.get("DEFAULT_LOCALE"),
            "production": request.META.get("PRODUCTION"),
            "platform": request.META.get("HTTP_SEC_CH_UA_PLATFORM"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
            "browser": request.META.get("HTTP_SEC_CH_UA"),
            "origin": request.META.get("HTTP_ORIGIN"),
            "referer": request.META.get("HTTP_REFERER"),
            "language": request.META.get("HTTP_ACCEPT_LANGUAGE"),
            "user_agent_os_family": user_agent.os.family,
            "user_agent_os_version": user_agent.os.version_string,
            "user_agent_device_family": user_agent.device.family,
            "user_agent_device_brand": user_agent.device.brand,
            "user_agent_device_model": user_agent.device.model,
            "user_agent_is_bot": user_agent.is_bot,
            "user_agent_is_pc": user_agent.is_pc,
            "user_agent_is_touch_capable": user_agent.is_touch_capable,
            "user_agent_is_tablet": user_agent.is_tablet,
            "user_agent_is_mobile": user_agent.is_mobile,
        }
