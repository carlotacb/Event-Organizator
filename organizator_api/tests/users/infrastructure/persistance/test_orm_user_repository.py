import uuid
from datetime import datetime

from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory

from app.users.infrastructure.persistance.orm_user_repository import ORMUserRepository
from app.users.infrastructure.persistance.models.orm_user import ORMUser
from app.users.domain.exceptions import UserAlreadyExists


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

