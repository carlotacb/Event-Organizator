import uuid
from datetime import datetime, timezone

from app.users.domain.models.user import UserRoles
from app.users.infrastructure.persistence.orm_user_repository import ORMUserRepository
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestORMUserRepositoryGetAll(ApiTests):
    def test__when_get_all__then_all_users_are_returned(self) -> None:
        # Given
        user = UserFactory().create(
            work=True,
            study=False,
            role=UserRoles.ORGANIZER,
            current_job_role="Software Engineer",
            university=None,
            degree=None,
            expected_graduation=None,
        )
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
        self.assertEqual(type(users[0].id), uuid.UUID)
        self.assertEqual(type(users[0].email), str)
        self.assertEqual(type(users[0].first_name), str)
        self.assertEqual(type(users[0].last_name), str)
        self.assertEqual(type(users[0].username), str)
        self.assertEqual(type(users[0].bio), str)
        self.assertEqual(type(users[0].profile_image), str)
        self.assertEqual(type(users[0].created_at), datetime)
        self.assertEqual(type(users[0].updated_at), datetime)

        self.assertEqual(users[0].id, uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"))
        self.assertEqual(users[0].email, "carlota@gmail.com")
        self.assertEqual(users[0].first_name, "Carlota")
        self.assertEqual(users[0].last_name, "Catot")
        self.assertEqual(users[0].username, "carlota2")
        self.assertEqual(users[0].bio, "The user that is using this application")
        self.assertEqual(users[0].profile_image, "profile_picture.png")
        self.assertEqual(users[0].role, UserRoles.PARTICIPANT)
        self.assertEqual(users[0].date_of_birth, datetime(1996, 5, 7, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(users[0].study, True)
        self.assertEqual(users[0].work, False)
        self.assertEqual(users[0].university, "Universitat Politècnica de Catalunya")
        self.assertEqual(users[0].degree, "Computer Science")
        self.assertEqual(users[0].expected_graduation, datetime(2024, 5, 1,0,0, tzinfo=timezone.utc))
        self.assertEqual(users[0].current_job_role, None)

        self.assertEqual(users[1].id, uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"))
        self.assertEqual(users[1].email, "carlota@hackupc.com")
        self.assertEqual(users[1].first_name, "Carlota")
        self.assertEqual(users[1].last_name, "Catot")
        self.assertEqual(users[1].username, "carlotacb")
        self.assertEqual(users[1].bio, "The user that is using this application")
        self.assertEqual(users[1].profile_image, "profile_picture.png")
        self.assertEqual(users[1].role, UserRoles.ORGANIZER)
        self.assertEqual(users[1].date_of_birth, datetime(1996, 5, 7, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(users[1].study, False)
        self.assertEqual(users[1].work, True)
        self.assertEqual(users[1].university, None)
        self.assertEqual(users[1].degree, None)
        self.assertEqual(users[1].expected_graduation, None)
        self.assertEqual(users[1].current_job_role, "Software Engineer")