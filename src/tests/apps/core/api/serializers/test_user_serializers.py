from unittest.mock import patch

from core.api.api_test_helpers import SerializerTestBase
from core.api.serializers import MeSerializer, RegisterSerializer, SimpleUserSerializer
from core.factories import UserFactory
from core.models import User
from rest_framework.exceptions import ValidationError


class SimpleUserSerializerTestCase(SerializerTestBase):
    def test_data(self):
        user: User = UserFactory()
        expected_data = {
            "uuid": user.uuid.hex,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        self.assertEqual(SimpleUserSerializer(user).data, expected_data)


class MeSerializerTestCase(SerializerTestBase):
    def test_data(self):
        user: User = UserFactory()
        expected_data = {
            "uuid": user.uuid.hex,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "birthdate": user.birthdate.isoformat(),
        }
        self.assertEqual(MeSerializer(user).data, expected_data)


class RegisterSerializerTestCase(SerializerTestBase):
    def test_data(self):
        user: User = UserFactory()
        expected_data = {
            "email": user.email,
        }
        self.assertIsNone(RegisterSerializer(user).data, expected_data)

    @patch("core.api.serializers.user_serializers.validators")
    def test_validate_password_ok(self, mock_validators):
        data_to_validate = {
            "email": "foo@foo.com",
            "password": "test_password",
        }
        serializer = RegisterSerializer(data=data_to_validate, context=self.context)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        self.assertEqual(mock_validators.validate_password.call_count, 1)

    def test_validate_password_similarity(self):
        previous_user: User = UserFactory()
        test_data_list = [
            (previous_user.email, "ThisIsARealValidPassword", "email", "unique"),
            (
                "foo@foopass.com",
                "foo@foopassword",
                "non_field_errors",
                "password_too_similar",
            ),
            ("foo@foopass.com", "short", "non_field_errors", "password_too_short"),
            ("foo@foopass.com", "1234567", "non_field_errors", "password_too_common"),
            (
                "foo@foopass.com",
                "141535876321858",
                "non_field_errors",
                "password_entirely_numeric",
            ),
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data):
                email, password, detail_key, expected_code = test_data
                data_to_validate = {
                    "email": email,
                    "password": password,
                }
                serializer = RegisterSerializer(data=data_to_validate, context=self.context)
                with self.assertRaises(ValidationError) as expected_error:
                    serializer.is_valid(raise_exception=True)
                self.assertEqual(
                    expected_error.exception.detail.get(detail_key)[0].code,
                    expected_code,
                )

    def test_create_user(self):
        self.assertEqual(User.objects.count(), 1)
        data_to_serializer = {
            "email": "foo@foo.com",
            "password": "ThisIsARealValidPassword",
        }
        serializer = RegisterSerializer(data=data_to_serializer, context=self.context)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        self.assertEqual(User.objects.count(), 2)
