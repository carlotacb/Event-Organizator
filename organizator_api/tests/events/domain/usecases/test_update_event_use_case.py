import uuid
from datetime import datetime

from app.events.application.requests import UpdateEventRequest
from app.events.domain.usecases.update_event_use_case import UpdateEventUseCase
from app.users.domain.exceptions import OnlyAuthorizedToOrganizer
from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestUpdateEventUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        event = EventFactory().create()
        self.event2_id = uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a")
        event2 = EventFactory().create(
            new_id=self.event2_id,
            name="HackUPC 2022",
        )
        self.event_repository.create(event)
        self.event_repository.create(event2)

        self.user_repository.clear()
        self.user_token = uuid.UUID("5b90906e-2894-467d-835e-3e4fbe42af9f")
        user = UserFactory().create(token=self.user_token, role=UserRoles.ORGANIZER)
        self.user_repository.create(user)

    def test__given_a_update_event_request_with_only_name__when_update_an_event_with_the_data__then_the_event_is_updated(
        self,
    ) -> None:
        # Given
        new_event = UpdateEventRequest(
            name="HackUPC 2021",
        )

        # When
        event = UpdateEventUseCase().execute(
            self.user_token,
            self.event2_id,
            new_event,
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
            start_date="15/10/2021 16:00",
            end_date="17/10/2021 16:00",
            location="The best city in the world",
        )

        # When
        event = UpdateEventUseCase().execute(
            self.user_token,
            self.event2_id,
            new_event,
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

    def test__given_a_update_event_request_with_a_participant_token__when_update_an_event__then_raise_exception(
        self,
    ) -> None:
        # Given
        new_event = UpdateEventRequest(
            name="HackUPC 2021",
        )
        user_token_part = uuid.UUID("fb95bfb6-3361-4628-8037-999d58b7183a")
        user_part = UserFactory().create(
            token=user_token_part,
            role=UserRoles.PARTICIPANT,
            new_id=uuid.UUID("5b90906e-2894-467d-835e-3e4fbe42af9e"),
            username="charlie",
            email="charlie@hackupc.com",
        )
        self.user_repository.create(user_part)

        # When
        with self.assertRaises(OnlyAuthorizedToOrganizer):
            UpdateEventUseCase().execute(
                user_token_part,
                self.event2_id,
                new_event,
            )
