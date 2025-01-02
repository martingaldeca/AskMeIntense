from unittest import mock

from core.factories import UserFactory
from core.models import User
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from questions.factories import (
    DislikedQuestionFactory,
    DislikedQuestionReactionFactory,
    FavoriteQuestionFactory,
    FavoriteQuestionReactionFactory,
    LikedQuestionFactory,
    LikedQuestionReactionFactory,
)
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

    def test_liked_reactions(self):
        user: User = UserFactory()
        reaction = LikedQuestionReactionFactory(user=user)
        self.assertEqual(list(user.liked_reactions), [reaction])

    def test_disliked_reactions(self):
        user: User = UserFactory()
        reaction = DislikedQuestionReactionFactory(user=user)
        self.assertEqual(list(user.disliked_reactions), [reaction])

    def test_favorite_reactions(self):
        user: User = UserFactory()
        reaction = FavoriteQuestionReactionFactory(user=user)
        self.assertEqual(list(user.favorite_reactions), [reaction])

    def test_liked_questions(self):
        user: User = UserFactory()
        question = LikedQuestionFactory(add_reaction__user=user)
        self.assertEqual(list(user.liked_questions), [question])

    def test_disliked_questions(self):
        user: User = UserFactory()
        question = DislikedQuestionFactory(add_reaction__user=user)
        self.assertEqual(list(user.disliked_questions), [question])

    def test_favorite_questions(self):
        user: User = UserFactory()
        question = FavoriteQuestionFactory(add_reaction__user=user)
        self.assertEqual(list(user.favorite_questions), [question])

    def test_is_liked_question(self):
        user: User = UserFactory()
        question = LikedQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_liked_question(question))

    def test_is_disliked_question(self):
        user: User = UserFactory()
        question = DislikedQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_disliked_question(question))

    def test_is_favorite_question(self):
        user: User = UserFactory()
        question = FavoriteQuestionFactory(add_reaction__user=user)
        self.assertTrue(user.is_favorite_question(question))
