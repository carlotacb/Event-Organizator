import uuid

from app.applications.domain.models.application import ApplicationStatus
from app.applications.domain.usecases.get_application_use_case import (
    GetApplicationUseCase,
)
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestGetApplicationUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.application_repository.clear()
        self.user_repository.clear()
        self.event_repository.clear()

        self.user_token_participant = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")

        self.user_participant = UserFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            token=self.user_token_participant,
            username="john",
            email="john@test.com",
        )
        self.user_repository.create(self.user_participant)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(new_id=self.event_id, name="HackUPC 2024")
        self.event_repository.create(self.event)

    def test__given_applications_in_db__when_get_application_using_the_id__then_returns_the_application_information(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
        )
        self.application_repository.create(application)

        # When
        application_information = GetApplicationUseCase().execute(
            application_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        )

        # Then
        self.assertEqual(
            application_information.id,
            uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
        )
        self.assertEqual(
            application_information.user.id,
            uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
        )
        self.assertEqual(
            application_information.event.id,
            uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
        )
        self.assertEqual(application_information.status, ApplicationStatus.PENDING)
