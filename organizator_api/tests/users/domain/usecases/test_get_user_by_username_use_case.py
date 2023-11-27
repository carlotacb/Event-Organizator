from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory

from app.users.domain.use_cases.get_user_by_username_use_case import (
    GetUserByUsernameUseCase,
)


class TestGetUserByUsernameUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

    def test__given_username__when_get_user_by_username__then_user_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)

        # When
        user = GetUserByUsernameUseCase().execute(username=user.username)

        # Then
        self.assertEqual(len(self.user_repository.get_all()), 1)
        self.assertEqual(user.id, user.id)
        self.assertEqual(user.email, user.email)
        self.assertEqual(user.password, user.password)
        self.assertEqual(user.first_name, user.first_name)
        self.assertEqual(user.last_name, user.last_name)
        self.assertEqual(user.username, user.username)
        self.assertEqual(user.bio, user.bio)
        self.assertEqual(user.profile_image, user.profile_image)
        self.assertEqual(user.created_at, user.created_at)
