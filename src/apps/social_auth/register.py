import os

from core.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class RegisterSocialUser:
    @classmethod
    def authenticate_or_register(cls, provider, user_data: dict):
        email = user_data.get("email")
        filtered_user_by_email = User.objects.filter(email=email)

        if (
            filtered_user_by_email.exists()
            and filtered_user_by_email[0].auth_provider != provider
        ):
            raise AuthenticationFailed(
                detail=filtered_user_by_email[0].not_valid_login_method_message
            )

        if not filtered_user_by_email.exists():
            user = {
                "email": email,
                "password": os.getenv("SOCIAL_AUTH_PASSWORD"),
                "is_verified": True,
                "auth_provider": provider,
                "first_name": user_data.get("given_name", ""),
                "last_name": user_data.get("family_name", ""),
            }
            if user_picture := user_data.get("picture"):
                user["picture_url"] = user_picture
            User.objects.create_user(**user)

        registered_user = authenticate(
            email=email, password=os.getenv("SOCIAL_AUTH_PASSWORD", "test_password")
        )
        return registered_user.tokens
