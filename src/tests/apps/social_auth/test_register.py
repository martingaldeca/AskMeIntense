import os
from unittest import mock
from unittest.mock import MagicMock, patch

from core.factories import VerifiedUserFactory
from core.models import User
from django.contrib.auth import authenticate
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from social_auth.register import RegisterSocialUser


class TestRegisterSocialUser(TestCase):

    def test_user_already_exists_with_other_auth_provider(self):
        test_data_list = [
            [
                User.AuthProviders.EMAIL_PROVIDER,
                User.AuthProviders.GOOGLE_PROVIDER,
                _("Please continue your login using email and password login"),
            ],
            [
                User.AuthProviders.GOOGLE_PROVIDER,
                User.AuthProviders.EMAIL_PROVIDER,
                _("Please continue your login using google login"),
            ],
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data), self.assertRaises(AuthenticationFailed) as expected_exception:
                previous_provider, used_provider, expected_exception_message = test_data
                user: User = VerifiedUserFactory(auth_provider=previous_provider)
                RegisterSocialUser.authenticate_or_register(provider=used_provider, user_data={"email": user.email})
            self.assertEqual(str(expected_exception.exception.detail), expected_exception_message)

    @patch("social_auth.register.authenticate")
    def test_create_user(self, mock_authenticate):
        mock_tokens = mock.MagicMock()
        mock_tokens.tokens = "test_token"
        mock_authenticate.return_value = mock_tokens
        self.assertEqual(User.objects.count(), 0)
        token = RegisterSocialUser.authenticate_or_register(
            provider=User.AuthProviders.GOOGLE_PROVIDER,
            user_data={
                "email": "test@test.com",
                "given_name": "test",
                "family_name": "test",
                "picture": "https://test.com",
            },
        )
        self.assertEqual(token, "test_token")
        self.assertEqual(User.objects.count(), 1)
        user: User = User.objects.last()
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.last_name, "test")
        self.assertEqual(user.auth_provider, User.AuthProviders.GOOGLE_PROVIDER)
        self.assertEqual(user.picture_url, "https://test.com")
        self.assertEqual(mock_authenticate.call_count, 1)
