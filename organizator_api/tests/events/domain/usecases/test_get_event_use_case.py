import uuid
from datetime import datetime

from app.events.domain.usecases.get_event_use_case import GetEventUseCase
from tests.events.domain.EventFactory import EventFactory
from tests.api_tests import ApiTests


class TestGetEventUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        event = EventFactory().create(
            new_id=uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a")
        )
        event2 = EventFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            name="HackUPC 2022",
        )
        self.event_repository.create(event)
        self.event_repository.create(event2)

    def test__given_events_in_the_database__when_get_an_event__then_all_the_events_are_returned(
        self,
    ) -> None:
        # When
        event = GetEventUseCase().execute(
            event_id=uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a")
        )

        # Then
        self.assertEqual(event.id, uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a"))
        self.assertEqual(type(event.id), uuid.UUID)
        self.assertEqual(event.name, "HackUPC 2023")
        self.assertEqual(type(event.name), str)
        self.assertEqual(event.description, "The biggest student hackathon in Europe")
        self.assertEqual(type(event.description), str)
        self.assertEqual(type(event.url), str)
        self.assertEqual(type(event.start_date), datetime)
        self.assertEqual(type(event.end_date), datetime)
        self.assertEqual(type(event.location), str)
        self.assertEqual(type(event.header_image), str)
        self.assertEqual(type(event.created_at), datetime)
        self.assertEqual(type(event.updated_at), datetime)
