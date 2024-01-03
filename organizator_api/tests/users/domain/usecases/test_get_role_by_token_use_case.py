import uuid

from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestGetRoleByTokenUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

    def test__given_token__when_get_role_by_token__then_role_is_returned(self) -> None:
        # Given
        user = UserFactory().create(
            token=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc")
        )
        self.user_repository.create(user)

        # When
        role_from_db = GetRoleByTokenUseCase().execute(token=user.token)

        # Then
        self.assertEqual(len(self.user_repository.get_all()), 1)
        self.assertEqual(role_from_db, user.role)
