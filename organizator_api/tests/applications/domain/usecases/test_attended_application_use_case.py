import uuid

from app.applications.domain.exceptions import (
    ApplicationNotFound,
    ApplicationCanNotBeAttended,
)
from app.applications.domain.models.application import ApplicationStatus
from app.applications.domain.usecases.attended_application_use_case import (
    AttendedApplicationUseCase,
)
from app.users.domain.exceptions import OnlyAuthorizedToOrganizer
from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestAttendedApplicationUseCase(ApiTests):
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
            role=UserRoles.ORGANIZER_ADMIN,
        )
        self.user_repository.create(self.user_organizer)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(new_id=self.event_id, name="HackUPC 2024")
        self.event_repository.create(self.event)

    def test__given_a_non_organizer_token__when_attended_application_use_case__then_only_authorized_to_organizer_admin(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(OnlyAuthorizedToOrganizer):
            AttendedApplicationUseCase().execute(
                application_id=uuid.uuid4(),
                token=self.user_token_participant,
            )

    def test__given_a_non_existing_application_id__when_attended_application_use_case__then_application_not_found_is_raised(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(ApplicationNotFound):
            AttendedApplicationUseCase().execute(
                application_id=uuid.uuid4(),
                token=self.user_token_organizer,
            )

    def test__given_a_application_id_of_a_invalid_application__when_attended_application_use_case__then_application_can_not_be_attended_is_raised(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
            status=ApplicationStatus.INVALID,
        )
        self.application_repository.create(application)

        # When
        with self.assertRaises(ApplicationCanNotBeAttended):
            AttendedApplicationUseCase().execute(
                application_id=application.id,
                token=self.user_token_organizer,
            )

    def test__given_a_application_id_of_a_rejected_application__when_attended_application_use_case__then_application_can_not_be_attended_is_raised(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
            status=ApplicationStatus.REJECTED,
        )
        self.application_repository.create(application)

        # When
        with self.assertRaises(ApplicationCanNotBeAttended):
            AttendedApplicationUseCase().execute(
                application_id=application.id,
                token=self.user_token_organizer,
            )

    def test__given_a_application_id_of_a_confirmed_application__when_attended_application_use_case__then_application_is_attended(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
            status=ApplicationStatus.CONFIRMED,
        )
        self.application_repository.create(application)

        # When
        AttendedApplicationUseCase().execute(
            application_id=application.id,
            token=self.user_token_organizer,
        )

        # Then
        self.assertEqual(
            ApplicationStatus.ATTENDED,
            self.application_repository.get(application_id=application.id).status,
        )
