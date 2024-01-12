import json
import uuid
from datetime import datetime, timezone

from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewUpdateApplicationStatus(ApiTests):
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

        self.user_token_organizer = "eb41b762-5988-4fa3-8942-7a91ccb00675"
        self.user_organizer = UserFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00675"),
            token=uuid.UUID(self.user_token_organizer),
            role=UserRoles.ORGANIZER_ADMIN,
        )
        self.user_repository.create(self.user_organizer)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(new_id=self.event_id, name="HackUPC 2024")
        self.event_repository.create(self.event)

    def test__when_update_application_status_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.post(
            "/organizator-api/applications/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_invalid_token__when_update_application_status__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.post(
            "/organizator-api/applications/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_valid_token_organizer_token_and_not_status_in_body__when_update_application_status__then_status_is_required_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.user_token_organizer}
        response = self.client.post(
            "/organizator-api/applications/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Status is required")

    def test__given_a_participant_token_and_body_with_status__when_update_application_status__then_only_authorized_to_organizer_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/applications/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            data=json.dumps({"status": "INVITED"}),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.content, b"Only admin users can change an application status"
        )

    def test__given_a_valid_token_organizer_token_and_a_non_existing_application__when_update_application_status__then_application_not_found_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.user_token_organizer}
        response = self.client.post(
            "/organizator-api/applications/update/eb41b762-5988-4fa3-8942-7a91ccb00687",
            data=json.dumps({"status": "INVITED"}),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Application not found")

    def test__given_a_non_existing_token_for_user_in_header__when_update_application_status__then_user_not_found_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": str(uuid.uuid4())}
        response = self.client.post(
            "/organizator-api/applications/update/eb41b762-5988-4fa3-8942-7a91ccb00687",
            data=json.dumps({"status": "INVITED"}),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User not found")

    def test__given_a_valid_token_organizer_token_and_a_existing_application__when_update_application_status__then_application_is_updated(
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
        headers = {"HTTP_Authorization": self.user_token_organizer}
        response = self.client.post(
            f"/organizator-api/applications/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            data=json.dumps({"status": "INVITED"}),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Application updated correctly")
