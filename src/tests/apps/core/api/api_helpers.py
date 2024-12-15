from rest_framework.test import APIRequestFactory, APITestCase


class APITestBase(APITestCase):
    """
    This class will be the base class for the api tests.

    Needed for the serializers to have context so the files can be well displayed.
    """

    url = None

    def setUp(self) -> None:
        self.request = APIRequestFactory().get(self.url)
        self.test_context = {"request": self.request}
