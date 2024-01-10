import uuid
from datetime import datetime

from app.events.domain.usecases.get_upcoming_events_and_participants_use_case import \
    GetUpcomingEventsAndParticipantsUseCase
from app.users.domain.exceptions import OnlyAuthorizedToOrganizer
from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestGetUpcomingEventAndParticipantsUseCase(ApiTests):
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
            role=UserRoles.ORGANIZER,
        )
        self.user_repository.create(self.user_organizer)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(
            new_id=self.event_id,
            name="HackUPC 2024",
            start_date=datetime(2025, 5, 12, 16, 0),
            end_date=datetime(2025, 5, 14, 18, 0),
        )
        self.event_repository.create(self.event)

        self.event_id2 = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00688")
        self.event2 = EventFactory().create(
            new_id=self.event_id2,
            name="HackUPC 2025",
            start_date=datetime(2026, 5, 12, 16, 0),
            end_date=datetime(2026, 5, 14, 18, 0),
        )
        self.event_repository.create(self.event2)

        self.application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
        )
        self.application_repository.create(self.application)

        self.application2 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00688"),
            event=self.event,
        )
        self.application_repository.create(self.application2)

        self.application3 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00681"),
            user=self.user_participant,
            event=self.event2,
        )
        self.application_repository.create(self.application3)

        self.application4 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00681"),
            event=self.event2,
        )
        self.application_repository.create(self.application4)


    def test__given_a_participant_token__when_get_upcoming_events_and_participants__then_only_authorized_to_organizer_is_raised(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(OnlyAuthorizedToOrganizer):
            GetUpcomingEventsAndParticipantsUseCase().execute(
                token=self.user_token_participant
            )

    def test__given_applications_in_the_db__when_get_upcoming_events_and_participants__then_a_list_of_applications_is_returned(
        self,
    ) -> None:
        # When
        response = GetUpcomingEventsAndParticipantsUseCase().execute(
            token=self.user_token_organizer
        )

        # Then
        self.assertEqual(len(response), 2)

        self.assertEqual(response[0].name, "HackUPC 2024")
        self.assertEqual(response[0].actual_participants_count, 2)
        self.assertEqual(response[0].max_participants, 100)
        self.assertEqual(response[0].expected_attrition_rate, 0.1)

        self.assertEqual(response[1].name, "HackUPC 2025")
        self.assertEqual(response[1].actual_participants_count, 2)
        self.assertEqual(response[1].max_participants, 100)
        self.assertEqual(response[1].expected_attrition_rate, 0.1)
