from app.users.domain.usecases.get_user_by_username_use_case import (
    GetUserByUsernameUseCase,
)
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


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
        user_from_db = GetUserByUsernameUseCase().execute(username=user.username)

        # Then
        self.assertEqual(len(self.user_repository.get_all()), 1)
        self.assertEqual(user_from_db.id, user.id)
        self.assertEqual(user_from_db.email, user.email)
        self.assertEqual(user_from_db.password, user.password)
        self.assertEqual(user_from_db.first_name, user.first_name)
        self.assertEqual(user_from_db.last_name, user.last_name)
        self.assertEqual(user_from_db.username, user.username)
        self.assertEqual(user_from_db.bio, user.bio)
        self.assertEqual(user_from_db.profile_image, user.profile_image)
        self.assertEqual(user_from_db.created_at, user.created_at)
