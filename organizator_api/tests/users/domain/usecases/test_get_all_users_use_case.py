import uuid

from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory
from app.users.domain.usecases.get_all_users_use_case import GetAllUsersUseCase


class TestGetAllUsersUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

    def test__given_users_in_the_database__when_get_all_users__then_all_the_users_are_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        user2 = UserFactory().create(
            new_id=uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a"),
            email="carlota@gmail.com",
            username="carlota2",
        )
        self.user_repository.create(user)
        self.user_repository.create(user2)

        # When
        users = GetAllUsersUseCase().execute()

        # Then
        self.assertEqual(len(users), 2)

    def test__given_no_user_in_db__when_get_all_users__then_an_empty_list_is_returned(
        self,
    ) -> None:
        # When
        users = GetAllUsersUseCase().execute()

        # Then
        self.assertEqual(len(users), 0)
