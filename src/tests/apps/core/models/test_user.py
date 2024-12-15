from unittest import mock

from core.factories import UserFactory
from core.models import User
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class UserTestCase(TestCase):
    def test_verify(self):
        user: User = UserFactory()
        self.assertFalse(user.is_verified)
        user.verify()
        user.refresh_from_db()
        self.assertTrue(user.is_verified)

    @mock.patch.object(RefreshToken, "for_user")
    def test_tokens(self, mock_refresh_token):
        user: User = UserFactory()
        refresh_token = mock.MagicMock()
        refresh_token.access_token = "test_access"
        refresh_token.__str__.return_value = "test_refresh"

        mock_refresh_token.return_value = refresh_token
        self.assertEqual(user.tokens, {"refresh": "test_refresh", "access": "test_access"})

    def test_not_valid_login_method_message(self):
        test_data_list = [
            (
                User.AuthProviders.EMAIL_PROVIDER,
                _("Please continue your login using email and password login"),
            ),
            (
                User.AuthProviders.GOOGLE_PROVIDER,
                _("Please continue your login using google login"),
            ),
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data):
                auth_provider, expected_message = test_data
                user: User = UserFactory(auth_provider=auth_provider)
                self.assertEqual(user.not_valid_login_method_message, expected_message)
