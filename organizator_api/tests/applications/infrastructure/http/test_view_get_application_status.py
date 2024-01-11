import uuid
from datetime import datetime, timezone

from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewGetApplicationStatus(ApiTests):
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

    def test__when_get_application_status_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get(
            "/organizator-api/applications/status/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_invalid_token__when_get_application_status__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.get(
            "/organizator-api/applications/status/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_valid_token_and_a_non_existing_event__when_get_application_status__then_event_not_found_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.get(
            "/organizator-api/applications/status/eb41b762-5988-4fa3-8942-7a91ccb00687",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Event not found")

    def test__given_a_exiting_event_and_a_token_for_a_non_existing_user__when_get_application_status__then_event_not_found_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": str(uuid.uuid4())}
        response = self.client.get(
            "/organizator-api/applications/status/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User not found")

    def test__given_a_existing_event_and_a_existing_user_but_any_application_for_that_relation__when_get_application_status__then_not_applied_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.get(
            "/organizator-api/applications/status/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 206)
        self.assertEqual(response.content, b"Not applied")

    def test__given_a_existing_event_and_a_existing_user_and_a_application_for_that_relation__when_get_application_status__then_applied_is_returned(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
            created_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
        )
        self.application_repository.create(application)

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.get(
            "/organizator-api/applications/status/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"status": "Under review"}')
