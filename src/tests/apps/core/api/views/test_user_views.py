from core.api.api_test_helpers import APITestBase, APITestBaseNeedAuthorized
from core.api.serializers import MeSerializer
from core.factories import UserFactory
from core.models import User
from django.urls import reverse
from rest_framework import status


class RegisterViewTestCase(APITestBase):
    url = reverse("core:register")

    def setUp(self):
        super().setUp()
        self.sent_data = {
            "email": "foo@foo.com",
            "password": "ThisIsARealValidPassword",
        }

    def test_post_create_user_201_created(self):
        self.client.logout()
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(self.url, data=self.sent_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_post_create_user_400_bad_request(self):
        self.client.logout()
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
                response = self.client.post(
                    self.url, data={"email": email, "password": password}
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data[detail_key][0].code, expected_code)


class MeDetailViewTestCase(APITestBaseNeedAuthorized):
    url = reverse("core:me")

    def test_get_me_detail_200_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MeSerializer(self.user).data)

    def test_patch_me_detail_200_ok(self):
        data_to_patch = {
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "email": "foo@foo.com",
            "birthdate": "1994-08-08",
            "avatar": "blue",
        }
        response = self.client.patch(self.url, data=data_to_patch)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        for key, value in data_to_patch.items():
            self.assertEqual(str(getattr(self.user, key)), value)

    def test_patch_me_detail_not_valid_email_400_bad_request(self):
        data_to_patch = {
            "email": "not_valid_email",
        }
        response = self.client.patch(self.url, data=data_to_patch)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
