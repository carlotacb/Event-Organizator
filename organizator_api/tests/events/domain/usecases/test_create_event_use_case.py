from datetime import datetime

from app.events.application.requests import CreateEventRequest
from app.events.domain.usecases.create_event_use_case import CreateEventUseCase
from tests.api_tests import ApiTests


class TestCreateEventUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()

    def test__given_create_event_request__when_create_event__then_the_event_is_created(
        self,
    ) -> None:
        # Given
        event_data = CreateEventRequest(
            name="HackNight Ep.VI",
            url="https://www.hacknights.dev",
            description="The best hack-night ever",
            start_date=datetime.strptime("2023-11-17T21:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            end_date=datetime.strptime("2023-11-18T05:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            location="Aula d'estudis Campus Nord",
            header_image="https://www.hacknights.dev/images/hacknight.png",
        )

        # When
        CreateEventUseCase().execute(event_data)

        # Then
        events = self.event_repository.get_all()
        self.assertEqual(len(events), 1)
