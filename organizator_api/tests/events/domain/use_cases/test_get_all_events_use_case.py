import uuid
from datetime import datetime, timezone

from tests.events.domain.EventFactory import EventFactory
from app.events.domain.use_cases.get_all_events_use_case import GetAllEventsUseCase
from tests.api_tests import ApiTests


class TestGetAllEventsUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        event = EventFactory().create()
        event2 = EventFactory().create(name="HackUPC 2022")
        self.event_repository.create(event)
        self.event_repository.create(event2)

    def test__given_events_in_the_database__when_get_all_event__then_all_the_events_are_returned(
        self,
    ) -> None:
        # When
        events = GetAllEventsUseCase().execute()

        # Then
        self.assertEqual(len(events), 2)
