import uuid
from datetime import datetime

from app.users.domain.exceptions import UserAlreadyExists, UserNotFound, UserNotLoggedIn
from app.users.domain.models.user import UserRoles
from app.users.infrastructure.persistence.models.orm_user import ORMUser
from app.users.infrastructure.persistence.orm_user_repository import ORMUserRepository
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestORMUserRepository(ApiTests):







    def test__given_a_user__when_update__then_user_is_updated(self) -> None:
        # Given
        user = UserFactory().create()
        ORMUserRepository().create(user=user)

        # When
        user.bio = "My name is Carlota and I love all the events I am going to"
        ORMUserRepository().update(user=user)

        # Then
        user = ORMUserRepository().get_by_id(user.id)
        self.assertEqual(
            user.bio, "My name is Carlota and I love all the events I am going to"
        )
        self.assertEqual(type(user.bio), str)

    def test__given_a_non_existing_user__when_update__then_user_not_found_is_raised(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()

        # Then
        with self.assertRaises(UserNotFound):
            ORMUserRepository().update(user=user)

    def test__given_a_user__when_update_with_a_username_that_already_exists__then_user_is_updated(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        ORMUserRepository().create(user=user)
        user2 = UserFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            email="carkbra@gmail.com",
            username="carlota2",
        )
        ORMUserRepository().create(user=user2)

        # When
        user2.username = "carlotacb"

        # Then
        with self.assertRaises(UserAlreadyExists):
            ORMUserRepository().update(user=user2)

    def test__given_a_user__when_update_role__then_role_is_updated(self) -> None:
        # Given
        user = UserFactory().create()
        ORMUserRepository().create(user=user)

        # When
        user.role = UserRoles.ORGANIZER
        ORMUserRepository().update(user=user)

        # Then
        user = ORMUserRepository().get_by_id(user.id)
        self.assertEqual(user.role, UserRoles.ORGANIZER)
