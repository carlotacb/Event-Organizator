import uuid
from datetime import datetime

from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory

from app.users.infrastructure.persistence.orm_user_repository import ORMUserRepository
from app.users.infrastructure.persistence.models.orm_user import ORMUser
from app.users.domain.exceptions import UserAlreadyExists, UserNotFound


class TestORMUserRepository(ApiTests):
    def test__given_a_user__when_create__then_user_is_saved(self) -> None:
        # Given
        user = UserFactory().create()

        # When
        ORMUserRepository().create(user=user)

        # Then
        self.assertIsNotNone(ORMUser.objects.get(id=str(user.id)))

    def test__given_a_user_that_already_exists__when_create__then_raise_exception(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        user2 = UserFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88")
        )
        ORMUserRepository().create(user=user)

        # Then
        with self.assertRaises(UserAlreadyExists):
            ORMUserRepository().create(user=user2)

    def test__when_get_all__then_all_users_are_returned(self) -> None:
        # Given
        user = UserFactory().create()
        user2 = UserFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            email="carlota@gmail.com",
            username="carlota2",
        )
        ORMUserRepository().create(user=user)
        ORMUserRepository().create(user=user2)

        # When
        users = ORMUserRepository().get_all()

        # Then
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].id, user.id)
        self.assertEqual(type(users[0].id), uuid.UUID)
        self.assertEqual(users[0].email, user.email)
        self.assertEqual(type(users[0].email), str)
        self.assertEqual(users[0].password, user.password)
        self.assertEqual(type(users[0].password), str)
        self.assertEqual(users[0].first_name, user.first_name)
        self.assertEqual(type(users[0].first_name), str)
        self.assertEqual(users[0].last_name, user.last_name)
        self.assertEqual(type(users[0].last_name), str)
        self.assertEqual(users[0].username, user.username)
        self.assertEqual(type(users[0].username), str)
        self.assertEqual(users[0].bio, user.bio)
        self.assertEqual(type(users[0].bio), str)
        self.assertEqual(users[0].profile_image, user.profile_image)
        self.assertEqual(type(users[0].profile_image), str)
        self.assertEqual(type(users[0].created_at), datetime)
        self.assertEqual(type(users[0].updated_at), datetime)
        self.assertEqual(users[1].id, user2.id)
        self.assertEqual(users[1].email, user2.email)
        self.assertEqual(users[1].password, user2.password)
        self.assertEqual(users[1].first_name, user2.first_name)
        self.assertEqual(users[1].last_name, user2.last_name)
        self.assertEqual(users[1].username, user2.username)
        self.assertEqual(users[1].bio, user2.bio)
        self.assertEqual(users[1].profile_image, user2.profile_image)

    def test__given_a_user__when_get_by_id__then_user_is_returned(self) -> None:
        # Given
        user = UserFactory().create()
        ORMUserRepository().create(user=user)

        # When
        user = ORMUserRepository().get_by_id(user.id)

        # Then
        self.assertEqual(user.id, user.id)
        self.assertEqual(type(user.id), uuid.UUID)
        self.assertEqual(user.email, user.email)
        self.assertEqual(type(user.email), str)
        self.assertEqual(user.password, user.password)
        self.assertEqual(type(user.password), str)
        self.assertEqual(user.first_name, user.first_name)
        self.assertEqual(type(user.first_name), str)
        self.assertEqual(user.last_name, user.last_name)
        self.assertEqual(type(user.last_name), str)
        self.assertEqual(user.username, user.username)
        self.assertEqual(type(user.username), str)
        self.assertEqual(user.bio, user.bio)
        self.assertEqual(type(user.bio), str)
        self.assertEqual(user.profile_image, user.profile_image)
        self.assertEqual(type(user.profile_image), str)
        self.assertEqual(type(user.created_at), datetime)
        self.assertEqual(type(user.updated_at), datetime)

    def test__given_a_non_existing_id__when_get_by_id__then_user_not_found_is_raised(
        self,
    ) -> None:
        # Then
        with self.assertRaises(UserNotFound):
            ORMUserRepository().get_by_id(uuid.uuid4())

    def test__given_a_user__when_get_by_username__then_user_is_returned(self) -> None:
        # Given
        user = UserFactory().create()
        ORMUserRepository().create(user=user)

        # When
        user = ORMUserRepository().get_by_username(user.username)

        # Then
        self.assertEqual(user.id, user.id)
        self.assertEqual(user.email, user.email)
        self.assertEqual(user.password, user.password)
        self.assertEqual(user.first_name, user.first_name)
        self.assertEqual(user.last_name, user.last_name)
        self.assertEqual(user.username, user.username)
        self.assertEqual(user.bio, user.bio)
        self.assertEqual(user.profile_image, user.profile_image)

    def test__given_a_non_existing_username__when_get_by_username__then_user_not_found_is_raised(
        self,
    ) -> None:
        # Then
        with self.assertRaises(UserNotFound):
            ORMUserRepository().get_by_username("non_existing_username")

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