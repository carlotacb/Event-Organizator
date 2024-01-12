import uuid
from datetime import datetime, timezone

from app.applications.domain.models.application import ApplicationStatus
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewCancelApplication(ApiTests):
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

    def test__when_cancel_application_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.post(
            "/organizator-api/applications/cancel/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_invalid_token__when_cancel_application__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.post(
            "/organizator-api/applications/cancel/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_non_existing_application_id__when_cancel_application__then_application_not_found_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/applications/cancel/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Application not found")

    def test__given_a_valid_application_id_with_invalid_status__when_cancel_application__then_application_can_not_be_cancelled_is_returned(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
            status=ApplicationStatus.INVALID,
            created_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
        )
        self.application_repository.create(application)

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/applications/cancel/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Application can not be cancelled")

    def test__given_a_valid_application_and_a_token_for_another_user__when_cancel_application__then_application_is_not_from_user_is_returned(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
            status=ApplicationStatus.PENDING,
            created_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
        )
        self.application_repository.create(application)

        user = UserFactory().create(
            token=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb01458"),
        )
        self.user_repository.create(user)

        # When
        headers = {"HTTP_Authorization": "eb41b762-5988-4fa3-8942-7a91ccb01458"}
        response = self.client.post(
            "/organizator-api/applications/cancel/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Application is not from user")

    def test__given_a_valid_application_id_with_invited_status__when_cancel_application__then_application_is_cancelled(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
            status=ApplicationStatus.INVITED,
            created_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 9, 10, 47, 0, tzinfo=timezone.utc),
        )
        self.application_repository.create(application)

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/applications/cancel/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Application is correctly cancelled")
