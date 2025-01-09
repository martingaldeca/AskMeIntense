import logging

from core.factories import VerifiedUserFactory
from core.models import User
from django.test.testcases import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase


class BaseTestCase(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        super().setUp()


class APITestBase(APITestCase):
    url = None

    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)
        if not self.url:
            self.skipTest("URL must be defined in subclasses.")
        self.user: User = VerifiedUserFactory(password="root1234")
        self.client.login(email=self.user.email, password="root1234")
        response = self.client.post(reverse("login"), {"email": self.user.email, "password": "root1234"})
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.request = APIRequestFactory().get(self.url)
        self.request.user = self.user
        self.test_context = {"request": self.request}
        super().setUp()


class APITestBaseNeedAuthorized(APITestBase):
    def test_not_logged_401_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"].code, "not_authenticated")


class SerializerTestBase(BaseTestCase):
    def setUp(self) -> None:
        self.user: User = VerifiedUserFactory()
        self.request = APIRequestFactory().post("/foo", data=None)
        self.request.user = self.user
        self.context = {"request": self.request}
        super().setUp()
