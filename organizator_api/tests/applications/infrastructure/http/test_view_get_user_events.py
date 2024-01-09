import uuid
from datetime import datetime, timezone

from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewGetUserEvents(ApiTests):
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

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(new_id=self.event_id, name="HackUPC 2024")
        self.event_repository.create(self.event)

    def test__when_get_user_events_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get(
            "/organizator-api/applications/myevents",
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_invalid_token__when_get_user_events__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.get(
            "/organizator-api/applications/myevents",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_non_existing_user_token__when_get_user_events__then_user_not_found_is_returned(
        self,
    ) -> None:
        # Given
        user_token = "eb41b762-5988-4fa3-8942-7a91ccb00688"

        # When
        headers = {"HTTP_Authorization": user_token}
        response = self.client.get(
            "/organizator-api/applications/myevents",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User not found")

    def test__given_a_valid_token_and_some_applications_for_a_user__when_get_user_events__then_user_events_are_returned(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            user=self.user_participant,
            event=self.event,
            created_at=datetime(2024, 1, 9, 0, 52, 29, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 9, 0, 52, 29, tzinfo=timezone.utc),
        )
        application2 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00687"),
            user=self.user_participant,
            created_at=datetime(2024, 1, 9, 0, 52, 29, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 9, 0, 52, 29, tzinfo=timezone.utc),
        )

        self.application_repository.create(application)
        self.application_repository.create(application2)

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.get(
            "/organizator-api/applications/myevents",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'[{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "event": {"id": "eb41b762-5988-4fa3-8942-7a91ccb00686", "name": "HackUPC 2024", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false, "open_for_participants": true, "max_participants": 100, "expected_attrition_rate": 0.1, "students_only": true, "age_restrictions": 16}, "created_at": "2024-01-09T00:52:29Z", "updated_at": "2024-01-09T00:52:29Z"}, {"id": "eb41b762-5988-4fa3-8942-7a91ccb00687", "event": {"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "name": "HackUPC 2023", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false, "open_for_participants": true, "max_participants": 100, "expected_attrition_rate": 0.1, "students_only": true, "age_restrictions": 16}, "created_at": "2024-01-09T00:52:29Z", "updated_at": "2024-01-09T00:52:29Z"}]'
        )
