import logging
import os

from core.models import User
from django.utils.translation import gettext_lazy as _
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from social_auth.register import RegisterSocialUser

logger = logging.getLogger(__name__)


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    @staticmethod
    def validate_auth_token(auth_token: str):
        user_data = verify_oauth2_token(auth_token, requests.Request())
        if os.getenv("DEBUG") != "True" and user_data.get("aud") != os.getenv("GOOGLE_OAUTH2_CLIENT_ID"):
            logger.error(
                "Not valid client from google authentication",
                extra={"auth_token": auth_token, "user_data": user_data},
            )
            raise AuthenticationFailed(detail=_("Not valid client"))

        return RegisterSocialUser.authenticate_or_register(provider=User.GOOGLE_PROVIDER, user_data=user_data)
