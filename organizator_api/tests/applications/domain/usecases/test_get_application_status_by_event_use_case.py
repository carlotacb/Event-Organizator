import uuid

from app.applications.domain.exceptions import (
    ApplicationNotFound,
    NotApplied,
    UserIsNotAParticipant,
)
from app.applications.domain.usecases.get_application_status_by_event_use_case import (
    GetApplicationStatusByEventUseCase,
)
from app.events.domain.exceptions import EventNotFound
from app.users.domain.exceptions import UserNotFound
from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestGetApplicationStatusByEventUseCase(ApiTests):
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

        self.user_token_organizer = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00675")

        self.user_organizer = UserFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00675"),
            token=self.user_token_organizer,
            role=UserRoles.ORGANIZER,
        )
        self.user_repository.create(self.user_organizer)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(new_id=self.event_id, name="HackUPC 2024")
        self.event_repository.create(self.event)

    def test__given_a_event_id_for_a_non_existing_event__when_get_application_status_by_event__then_event_not_found_is_raised(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(EventNotFound):
            GetApplicationStatusByEventUseCase().execute(
                event_id=uuid.uuid4(), token=self.user_token_participant
            )

    def test__given_a_token_for_a_non_existing_user__when_get_application_status_by_event__then_user_not_found_is_raised(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(UserNotFound):
            GetApplicationStatusByEventUseCase().execute(
                event_id=self.event_id, token=uuid.uuid4()
            )

    def test__given_a_correct_participant_token_and_event_id_for_a_non_existing_application__when_get_application_status_by_event__then_not_applied_is_raised(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(NotApplied):
            GetApplicationStatusByEventUseCase().execute(
                event_id=self.event_id, token=self.user_token_participant
            )

    def test__given_a_correct_organizer_token_and_event_id_for_a_non_existing_application__when_get_application_status_by_event__then_not_applied_is_raised(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(UserIsNotAParticipant):
            GetApplicationStatusByEventUseCase().execute(
                event_id=self.event_id, token=self.user_token_organizer
            )

    def test__given_a_correct_token_and_event_id_for_a_existing_applications__when_get_application_status_by_event__then_application_status_is_returned(
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
        application_status = GetApplicationStatusByEventUseCase().execute(
            event_id=self.event_id, token=self.user_token_participant
        )

        # Then
        self.assertEqual(application_status, application.status)
