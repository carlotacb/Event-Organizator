import uuid
from datetime import datetime

from app.events.application.requests import UpdateEventRequest
from app.events.domain.usecases.update_event_use_case import UpdateEventUseCase
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory


class TestUpdateEventUseCase(ApiTests):
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

    def test__given_a_update_event_request_with_only_name__when_update_an_event_with_the_data__then_the_event_is_updated(
        self,
    ) -> None:
        # Given
        new_event = UpdateEventRequest(
            name="HackUPC 2021",
        )

        # When
        event = UpdateEventUseCase().execute(
            uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a"), new_event
        )

        # Then
        self.assertEqual(event.name, "HackUPC 2021")

    def test__given_a_update_event_request_with_all_data__when_update_an_event_with_the_data__then_the_event_is_updated(
        self,
    ) -> None:
        # Given
        new_event = UpdateEventRequest(
            name="HackUPC 2021",
            description="Hackathon in Barcelona 2021",
            url="https://2021.hackupc.com",
            start_date=datetime.strptime("2021-10-15T16:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            end_date=datetime.strptime("2021-10-17T16:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            location="The best city in the world",
        )

        # When
        event = UpdateEventUseCase().execute(
            uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a"), new_event
        )

        # Then
        self.assertEqual(event.name, "HackUPC 2021")
        self.assertEqual(event.description, "Hackathon in Barcelona 2021")
        self.assertEqual(event.url, "https://2021.hackupc.com")
        self.assertEqual(
            event.start_date,
            datetime.strptime("2021-10-15T16:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(
            event.end_date,
            datetime.strptime("2021-10-17T16:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(event.location, "The best city in the world")
