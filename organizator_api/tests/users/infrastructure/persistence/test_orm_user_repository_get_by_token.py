import uuid
from datetime import datetime, timezone

from app.users.domain.exceptions import UserNotLoggedIn, UserNotFound
from app.users.domain.models.user import UserRoles
from app.users.infrastructure.persistence.orm_user_repository import ORMUserRepository
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestORMUserRepositoryGetByToken(ApiTests):
    def test__given_a_user__when_get_by_token__then_user_is_returned(self) -> None:
        # Given
        user_to_created = UserFactory().create(
            token=uuid.UUID("8e0af048-073a-47e7-8de8-db7a17718e95")
        )
        ORMUserRepository().create(user=user_to_created)

        # When
        user = ORMUserRepository().get_by_token(user_to_created.token)

        # Then
        self.assertEqual(user.id, uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"))
        self.assertEqual(user.email, "carlota@hackupc.com")
        self.assertEqual(user.first_name, "Carlota")
        self.assertEqual(user.last_name, "Catot")
        self.assertEqual(user.username, "carlotacb")
        self.assertEqual(user.bio, "The user that is using this application")
        self.assertEqual(user.profile_image, "profile_picture.png")
        self.assertEqual(user.token, uuid.UUID("8e0af048-073a-47e7-8de8-db7a17718e95"))
        self.assertEqual(user.role, UserRoles.PARTICIPANT)
        self.assertEqual(user.date_of_birth, datetime(1996, 5, 7, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(user.study, True)
        self.assertEqual(user.work, False)
        self.assertEqual(user.university, "Universitat Politècnica de Catalunya")
        self.assertEqual(user.degree, "Computer Science")
        self.assertEqual(user.expected_graduation, datetime(2024, 5, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(user.current_job_role, None)
        self.assertEqual(user.tshirt, None)
        self.assertEqual(user.gender, None)
        self.assertEqual(user.alimentary_restrictions, None)
        self.assertEqual(user.github, None)
        self.assertEqual(user.linkedin, None)
        self.assertEqual(user.devpost, None)
        self.assertEqual(user.webpage, None)

    def test__when_get_by_token_is_called_without_a_token__then_user_not_logged_in_is_raised(
            self,
    ) -> None:
        # Then
        with self.assertRaises(UserNotLoggedIn):
            ORMUserRepository().get_by_token(None)

    def test__given_a_non_existing_token__when_get_by_token__then_user_not_found_is_raised(
            self,
    ) -> None:
        # Then
        with self.assertRaises(UserNotFound):
            ORMUserRepository().get_by_token(
                uuid.UUID("8e0af048-073a-47e7-8de8-db7a17718e95")
            )