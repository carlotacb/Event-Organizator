import uuid

from app.users.domain.usecases.logout_use_case import LogoutUseCase
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestLogoutUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

    def test__given_a_user_with_a_valid_token__when_logout__then_the_user_token_is_deleted(
        self,
    ) -> None:
        # Given
        token_for_user = uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d")
        user = UserFactory().create(token=token_for_user)
        self.user_repository.create(user)

        # When
        LogoutUseCase().execute(token=token_for_user)

        # Then
        user = self.user_repository.get_all()[0]
        self.assertIsNone(user.token)
