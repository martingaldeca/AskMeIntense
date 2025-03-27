from data.events import events
from data.exceptions import NotValidEventException
from django.contrib.auth.models import User
from rest_framework import serializers


class DataEventSerializer(serializers.Serializer):
    event_type = serializers.CharField(required=True)
    app_version = serializers.CharField(required=True)
    extra_info = serializers.JSONField(required=False)

    def is_valid(self, raise_exception=False, user: User = None):
        validation = super().is_valid(raise_exception=raise_exception)

        if event_type := self.validated_data["event_type"] not in events.keys():
            raise NotValidEventException(event_type)
        if user and not user.is_anonymous:
            self.validated_data["user_identifier"] = user.uuid.hex
        return validation
