import uuid

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
