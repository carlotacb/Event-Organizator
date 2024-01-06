import uuid
from datetime import datetime, timezone

from app.users.domain.exceptions import UserNotFound
from app.users.domain.models.user import UserRoles
from app.users.infrastructure.persistence.orm_user_repository import ORMUserRepository
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestORMUserRepositoryGetById(ApiTests):
    def test__given_a_user__when_get_by_id__then_user_is_returned(self) -> None:
        # Given
        user_to_create = UserFactory().create()
        ORMUserRepository().create(user=user_to_create)

        # When
        user = ORMUserRepository().get_by_id(user_to_create.id)

        # Then
        self.assertEqual(type(user.id), uuid.UUID)
        self.assertEqual(type(user.email), str)
        self.assertEqual(type(user.password), bytes)
        self.assertEqual(type(user.first_name), str)
        self.assertEqual(type(user.last_name), str)
        self.assertEqual(type(user.username), str)
        self.assertEqual(type(user.bio), str)
        self.assertEqual(type(user.profile_image), str)
        self.assertEqual(type(user.created_at), datetime)
        self.assertEqual(type(user.updated_at), datetime)

        self.assertEqual(user.id, uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"))
        self.assertEqual(user.email, "carlota@hackupc.com")
        self.assertEqual(user.first_name, "Carlota")
        self.assertEqual(user.last_name, "Catot")
        self.assertEqual(user.username, "carlotacb")
        self.assertEqual(user.bio, "The user that is using this application")
        self.assertEqual(user.profile_image, "profile_picture.png")
        self.assertEqual(user.token, None)
        self.assertEqual(user.role, UserRoles.PARTICIPANT)
        self.assertEqual(
            user.date_of_birth, datetime(1996, 5, 7, 0, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(user.study, True)
        self.assertEqual(user.work, False)
        self.assertEqual(user.university, "Universitat Politècnica de Catalunya")
        self.assertEqual(user.degree, "Computer Science")
        self.assertEqual(
            user.expected_graduation, datetime(2024, 5, 1, 0, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(user.current_job_role, None)
        self.assertEqual(user.tshirt, None)
        self.assertEqual(user.gender, None)
        self.assertEqual(user.alimentary_restrictions, None)
        self.assertEqual(user.github, None)
        self.assertEqual(user.linkedin, None)
        self.assertEqual(user.devpost, None)
        self.assertEqual(user.webpage, None)

    def test__given_a_non_existing_id__when_get_by_id__then_user_not_found_is_raised(
        self,
    ) -> None:
        # Then
        with self.assertRaises(UserNotFound):
            ORMUserRepository().get_by_id(uuid.uuid4())
