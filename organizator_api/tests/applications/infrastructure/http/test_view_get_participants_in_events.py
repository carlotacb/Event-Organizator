import uuid
from datetime import datetime, timezone

from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewGetParticipantsInEvents(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.application_repository.clear()
        self.user_repository.clear()
        self.event_repository.clear()

        self.user_token_participant = "eb41b762-5988-4fa3-8942-7a91ccb00686"
        self.user_participant = UserFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            token=uuid.UUID(self.user_token_participant),
            username="john",
            email="john@test.com",
        )
        self.user_repository.create(self.user_participant)

        self.user_token_organizer = "eb41b762-5988-4fa3-8942-7a91ccb00687"
        user_organizer = UserFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00687"),
            token=uuid.UUID(self.user_token_organizer),
            username="jane",
            email="jane@test.com",
            role=UserRoles.ORGANIZER,
        )
        self.user_repository.create(user_organizer)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(new_id=self.event_id, name="HackUPC 2024")
        self.event_repository.create(self.event)

    def test__when_get_participants_in_events_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get(
            "/organizator-api/applications/participants/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_invalid_token__when_get_participants_in_events__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.get(
            "/organizator-api/applications/participants/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_non_existing_event_token__when_get_participants_in_events__then_event_not_found_is_returned(
        self,
    ) -> None:
        # Given
        headers = {"HTTP_Authorization": self.user_token_organizer}

        # When
        response = self.client.get(
            "/organizator-api/applications/participants/eb41b762-5988-4fa3-8942-7a91ccb00685",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.content, b"Event not found")
        self.assertEqual(response.status_code, 404)

    def test__given_a_participant_user_and_a_existing_event__when_get_participants_in_events__then_only_authorized_to_organizers_is_returned(
        self,
    ) -> None:
        # Given
        headers = {"HTTP_Authorization": self.user_token_participant}

        # When
        response = self.client.get(
            "/organizator-api/applications/participants/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.content, b"Only authorized to organizer")
        self.assertEqual(response.status_code, 401)

    def test__given_a_organizer_user_and_a_existing_event_without_participants__when_get_participants_in_events__then_empty_list_is_returned(
        self,
    ) -> None:
        # Given
        headers = {"HTTP_Authorization": self.user_token_organizer}

        # When
        response = self.client.get(
            "/organizator-api/applications/participants/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")

    def test__given_a_organizer_user_and_a_existing_event_with_participants__when_get_participants_in_events__then_participants_list_is_returned(
        self,
    ) -> None:
        # Given
        application1 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
            created_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
        )
        application2 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00687"),
            event=self.event,
            created_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
        )
        self.application_repository.create(application1)
        self.application_repository.create(application2)

        headers = {"HTTP_Authorization": self.user_token_organizer}

        # When
        response = self.client.get(
            "/organizator-api/applications/participants/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'[{"id": "eb41b762-5988-4fa3-8942-7a91ccb00686", "user": {"id": "eb41b762-5988-4fa3-8942-7a91ccb00686", "username": "john", "email": "john@test.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "profile_picture.png", "role": "Participant", "date_of_birth": "07/05/1996", "study": true, "work": false, "university": "Universitat Polit\\u00e8cnica de Catalunya", "degree": "Computer Science", "expected_graduation": "01/05/2024", "current_job_role": "", "tshirt": "", "gender": "", "alimentary_restrictions": "", "github": "", "linkedin": "", "devpost": "", "webpage": ""}, "status": "Under review", "created_at": "2024-01-09T10:47:00Z", "updated_at": "2024-01-09T10:47:00Z"}, {"id": "eb41b762-5988-4fa3-8942-7a91ccb00687", "user": {"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "profile_picture.png", "role": "Participant", "date_of_birth": "07/05/1996", "study": true, "work": false, "university": "Universitat Polit\\u00e8cnica de Catalunya", "degree": "Computer Science", "expected_graduation": "01/05/2024", "current_job_role": "", "tshirt": "", "gender": "", "alimentary_restrictions": "", "github": "", "linkedin": "", "devpost": "", "webpage": ""}, "status": "Under review", "created_at": "2024-01-09T10:47:00Z", "updated_at": "2024-01-09T10:47:00Z"}]',
        )
