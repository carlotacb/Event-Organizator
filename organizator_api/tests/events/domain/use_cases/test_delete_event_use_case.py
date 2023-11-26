import uuid

from app.events.domain.use_cases.delete_event_use_case import DeleteEventUseCase
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory


class TestDeleteEventUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        event = EventFactory().create(
            new_id=uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a"),
            name="HackUPC 2022",
        )
        self.event_repository.create(event)

    def test__given_events_in_db__when_delete_use_case__then_(self) -> None:
        # Given
        event_id = uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a")

        # When
        DeleteEventUseCase().execute(event_id)

        # Then
        event = self.event_repository.get(event_id)
        self.assertIsNotNone(event.deleted_at)
        self.assertEqual(event.deleted_at, event.updated_at)
