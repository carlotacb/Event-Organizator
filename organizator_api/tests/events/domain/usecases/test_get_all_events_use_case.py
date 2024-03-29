import uuid

from app.events.domain.usecases.get_all_events_use_case import GetAllEventsUseCase
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory


class TestGetAllEventsUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        event = EventFactory().create()
        event2 = EventFactory().create(
            new_id=uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a"),
            name="HackUPC 2022",
        )
        self.event_repository.create(event)
        self.event_repository.create(event2)

    def test__given_events_in_the_database__when_get_all_event__then_all_the_events_are_returned(
        self,
    ) -> None:
        # When
        events = GetAllEventsUseCase().execute()

        # Then
        self.assertEqual(len(events), 2)
