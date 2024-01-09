import uuid

from app.applications.domain.usecases.get_applications_by_token_use_case import (
    GetApplicationsByTokenUseCase,
)
from app.users.domain.exceptions import UserNotFound
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestGetApplicationsByTokenUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.application_repository.clear()
        self.user_repository.clear()
        self.event_repository.clear()

        self.user_token_participant = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.user_token_organizer = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00687")

        self.user_participant = UserFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            token=self.user_token_participant,
            username="john",
            email="john@test.com",
        )
        self.user_repository.create(self.user_participant)

        self.user_organizer = UserFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00687"),
            token=self.user_token_organizer,
            username="jane",
            email="jane@test.com",
        )
        self.user_repository.create(self.user_organizer)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(new_id=self.event_id, name="HackUPC 2024")
        self.event_repository.create(self.event)

    def test__given_a_invalid_token__when_get_application_by_token__then_user_not_found_is_raised(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(UserNotFound):
            GetApplicationsByTokenUseCase().execute(token=uuid.uuid4())

    def test__given_applications_in_the_bd__when_get_applications_by_token__then_a_list_of_applications_is_returned(
        self,
    ) -> None:
        # Given
        application1 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
        )
        application2 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00687"),
            event=self.event,
            user=self.user_participant,
        )
        application3 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00688"),
            event=self.event,
            user=self.user_organizer,
        )

        self.application_repository.create(application1)
        self.application_repository.create(application2)
        self.application_repository.create(application3)

        # When
        applications = GetApplicationsByTokenUseCase().execute(
            token=self.user_token_participant
        )

        # Then
        self.assertEqual(len(applications), 2)
        self.assertEqual(applications[0].event.name, "HackUPC 2023")
        self.assertEqual(applications[1].event.name, "HackUPC 2024")
