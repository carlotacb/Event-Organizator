import uuid

from app.applications.domain.exceptions import (
    ApplicationNotFound,
    ApplicationCanNotBeCancelled,
    ApplicationIsNotFromUser,
)
from app.applications.domain.models.application import ApplicationStatus
from app.applications.domain.usecases.cancel_application_use_case import (
    CancelApplicationUseCase,
)
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestCancelApplicationUseCase(ApiTests):
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

    def test__given_a_non_existing_application_id__when_cancel_application__then_application_not_found_is_raised(
        self,
    ) -> None:
        # When
        with self.assertRaises(ApplicationNotFound):
            CancelApplicationUseCase().execute(
                application_id=uuid.uuid4(),
                token=self.user_token_participant,
            )

    def test__given_a_application_id_of_a_invalid_application__when_cancel_application__then_application_can_not_be_cancelled_is_raised(
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
        with self.assertRaises(ApplicationCanNotBeCancelled):
            CancelApplicationUseCase().execute(
                application_id=application.id,
                token=self.user_token_participant,
            )

    def test__given_a_application_id_of_a_rejected_application__when_cancel_application__then_application_can_not_be_cancelled_is_raised(
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
        with self.assertRaises(ApplicationCanNotBeCancelled):
            CancelApplicationUseCase().execute(
                application_id=application.id,
                token=self.user_token_participant,
            )

    def test__given_a_application_id_of_a_attended_application__when_cancel_application__then_application_can_not_be_cancelled_is_raised(
        self,
    ) -> None:
        # Given
        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
            status=ApplicationStatus.ATTENDED,
        )
        self.application_repository.create(application)

        # When
        with self.assertRaises(ApplicationCanNotBeCancelled):
            CancelApplicationUseCase().execute(
                application_id=application.id,
                token=self.user_token_participant,
            )

    def test__given_a_application_id_and_a_token_from_another_user__when_cancel_application__then_application_is_not_from_user(
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
        with self.assertRaises(ApplicationIsNotFromUser):
            CancelApplicationUseCase().execute(
                application_id=application.id,
                token=uuid.uuid4(),
            )

    def test__given_a_application_with_accepted_status__when_cancel_application__then_application_is_cancelled(
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
        CancelApplicationUseCase().execute(
            application_id=application.id,
            token=self.user_token_participant,
        )

        # Then
        self.assertEqual(
            ApplicationStatus.CANCELLED,
            self.application_repository.get(application_id=application.id).status,
        )
