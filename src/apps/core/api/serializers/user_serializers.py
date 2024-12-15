import logging

import django.contrib.auth.password_validation as validators
from core.helpers import UUIDModelSerializerMixin
from core.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class SimpleUserSerializer(UUIDModelSerializerMixin):
    class Meta:
        model = User
        fields = ["uuid", "email", "first_name", "last_name"]


class MeSerializer(SimpleUserSerializer):
    class Meta:
        model = User
        fields = [
            "uuid",
            "first_name",
            "last_name",
            "email",
            "birthdate",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")
        errors = {}
        try:
            validators.validate_password(password=password, user=user)
        except ValidationError as exception:
            errors["password"] = list(str(exception))
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)

    @staticmethod
    def create(validated_data):  # pylint: disable=E1134, W0221
        return User.objects.create_user(**validated_data)  # pylint: disable=W0221

    @property
    def data(self):
        return None
