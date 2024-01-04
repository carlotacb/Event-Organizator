import uuid

from app.events.domain.usecases.delete_event_use_case import DeleteEventUseCase
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestDeleteEventUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        event = EventFactory().create(
            new_id=uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a"),
            name="HackUPC 2022",
        )
        self.event_repository.create(event)
        self.user_repository.clear()

    def test__given_events_in_db__when_delete_use_case__then_the_event_is_deleted(
        self,
    ) -> None:
        # Given
        user_token = uuid.UUID("5b90906e-2894-467d-835e-3e4fbe42af9f")
        user = UserFactory().create(token=user_token, role=UserRoles.ORGANIZER_ADMIN)
        self.user_repository.create(user)
        event_id = uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a")

        # When
        DeleteEventUseCase().execute(user_token, event_id)

        # Then
        event = self.event_repository.get(event_id)
        self.assertIsNotNone(event.deleted_at)
        self.assertEqual(event.deleted_at, event.updated_at)

    def test__given_events_in_db__when_delete_use_case_with_a_token_participant__then_exception_is_raised(
        self,
    ) -> None:
        # Given
        user_token = uuid.UUID("5b90906e-2894-467d-835e-3e4fbe42af9f")
        user = UserFactory().create(token=user_token, role=UserRoles.PARTICIPANT)
        self.user_repository.create(user)
        event_id = uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a")

        # When / Then
        with self.assertRaises(OnlyAuthorizedToOrganizerAdmin):
            DeleteEventUseCase().execute(user_token, event_id)
