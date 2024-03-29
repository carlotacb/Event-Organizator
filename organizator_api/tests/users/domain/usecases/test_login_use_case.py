import uuid

from app.users.domain.exceptions import InvalidPassword
from app.users.domain.usecases.login_use_case import LoginUseCase
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestLoginUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

    def test__given_username_and_password__when_login__then_user_have_a_valid_token(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)

        # When
        token = LoginUseCase().execute(username=user.username, password="123456")

        # Then
        user = self.user_repository.get_all()[0]
        self.assertIsNotNone(user.token)
        self.assertEqual(token, user.token)

    def test__given_username_and_a_invalid_password__when_login__then_it_raises_invalid_password(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)

        # When
        with self.assertRaises(InvalidPassword):
            LoginUseCase().execute(
                username=user.username, password="this is not a valid password"
            )

    def test__given_a_user_with_a_token_already__when_login__then_it_returns_the_existing_token(
        self,
    ) -> None:
        # Given
        user = UserFactory().create(
            token=uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d")
        )
        self.user_repository.create(user)

        # When
        token = LoginUseCase().execute(username=user.username, password="123456")

        # Then
        user = self.user_repository.get_all()[0]
        self.assertEqual(token, uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"))
        self.assertEqual(token, user.token)

    def test__given_a_username_with_uppercase_letters_and_a_valid_password__then_when_login__then_the_user_have_a_valid_token(
        self,
    ) -> None:
        # Given
        user = UserFactory().create(username="carlota")
        self.user_repository.create(user)

        # When
        token = LoginUseCase().execute(username="Carlota", password="123456")

        # Then
        user = self.user_repository.get_all()[0]
        self.assertIsNotNone(user.token)
        self.assertEqual(token, user.token)
